"""Unit tests for the fattybugs database"""

import unittest
import fattybugs
import datetime
import os
import configparser

class TestBugDB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        if os.getenv("HOME"):
            cls.db_file=os.path.join(os.getenv("HOME"),"test_db_file")
        else:
            cls.db_file=os.path.join(os.getenv("USERPROFILE"),"test_db_file")
        
        #remove the existing test file
        if os.path.isfile(cls.db_file):
            os.remove(cls.db_file)

        #create the new file
        fattybugs.build_db(cls.db_file)

        #initialize the bug database
        cls.BugDB=fattybugs.BugDB(cls.db_file)

    @classmethod
    def tearDownClass(cls):
        cls.BugDB.cxn.close()

        os.remove(cls.db_file)

    def tearDown(self):
        
        cur=self.BugDB.cxn.cursor()
        cur.execute("DELETE FROM bugs")
        self.BugDB.cxn.commit()

    def test_new_bug(self):
        lastrowid=self._insert_data()

        self.assertGreaterEqual(lastrowid,0)
        cur=self.BugDB.cxn.cursor()
        row=cur.execute("""SELECT * FROM bugs WHERE ROWID=?""",(lastrowid,)).fetchone()
        desired_data=self._default_insert_data()
        for k in desired_data.keys():
            self.assertEqual(desired_data[k],row[k])                              

    def test_all_bug_data(self):
        """test bugs() method for BugDB"""
        cur=self.BugDB.cxn.cursor()
        wanted_data=self._default_multi_insert_data()
        for row in wanted_data:
            self._insert_data(row)
        
        data=list(self.BugDB.bugs())

        for i,row in enumerate(wanted_data): 
            for k in row.keys():
                self.assertEqual(row[k],data[i][k])
    def test_bug_data(self):
        newid=self._insert_data()
        bug_data=self.BugDB.bug_data(bug_id=newid)
        desired_data=self._default_insert_data()
        for k in desired_data.keys():
            self.assertEqual(desired_data[k],bug_data[k])                                     

    def test_reassign(self):
        newid=self._insert_data()
        self.BugDB.reassign("reassigned",bug_id=newid)
        data=self.BugDB.bug_data(bug_id=newid)
        self.assertEqual(data["assigned_to"],"reassigned")
    
    def test_fix_bug(self):
        newid=self._insert_data()
        
        self.BugDB.fix_bug(bug_id=newid)

        q="SELECT {} FROM {} WHERE ROWID=? AND {}=0".format(self.BugDB.NAME_COLUMN,self.BugDB.BUG_TABLE,self.BugDB.FIXED_COLUMN)
        params=(newid,)
        cur=self.BugDB.cxn.cursor()
        cur.execute(q,params)
        rows=cur.fetchall()
        self.assertEqual(len(rows),0)                

    def test_default_db(self):
        c=configparser.ConfigParser()
        db_file=None
        rm_configs=False
        rm_section=True
        rm_option=True
        if os.path.isfile(fattybugs._default_configfile()):
            with open(fattybugs._default_configfile()) as cfh:
                c.read(cfh)
                
            if "bug_db" not in c.sections():
                rm_section=True                
                c.add_section("bug_db")
            if "db_file" in c.options("bug_db"):
                db_file=c.get("bug_db","db_file")
            else:
                rm_option=True
                if os.getenv("HOME"):

                    db_file=os.path.join(os.getenv("HOME"),"test_db_default.db")
                elif os.getenv("USERPROFILE"):
                    db_file=os.path.join(os.getenv("USERPROFILE"),"test_db_default.db")
                else:
                    raise Exception("HOME or USERPROFILE environment variable must be ste")
                c.set("bug_db","db_file",db_file)
                with open(fattybugs._default_configfile(),"a") as cfh:
                    c.write(cfh)                    
                    
        else:
            rm_configs=True
            with open(fattybugs._default_configfile(),"w") as cfh:
                c.add_section("bug_db")
                dbfile=None
                if os.getenv("HOME"):
                    
                    db_file=os.path.join(os.getenv("HOME"),"test_db_default.db")
                elif os.getenv("USERPROFILE"):
                    db_file=os.path.join(os.getenv("USERPROFILE"),"test_db_default.db")
                else:
                    raise Exception("HOME or USERPROFILE environment variable must be ste")
                c.set("bug_db","db_file",db_file)
                c.write(cfh)

        dbdb=fattybugs.default_bug_db()
        self.assertEqual(dbdb,db_file)
        self.assertTrue(type(fattybugs.default_BugDB()) is fattybugs.BugDB)
        self.assertEqual(fattybugs.default_BugDB().filename,db_file)
        if rm_option:
            c.remove_option("bug_db","db_file")
        if rm_section:
            c.remove_section("bug_db")
        if rm_configs:
            os.remove(fattybugs._default_configfile())    

    # def test_bug_details_display(self):
    #     new_id=self._insert_data()
    #     self.BugDB.bug_details_display(bug_id=new_id)
        
    def test_build_db(self):
        new_db=None
        if os.getenv("HOME"):
            new_db=os.path.join(os.getenv("HOME"),"new_test_db.db")
        elif os.getenv("USERPROFILE"):
            new_db=os.path.join(os.getenv("USERPROFILE"),"new_test_db.db")
        else:
            raise Exception("HOME or USERPROFILE environment variable must be ste")

        new_configfile=new_db+".config"
        for f in (new_db,new_configfile):
            if os.path.isfile(f):
                os.remove(f)
        fattybugs.build_db(new_db,True,new_configfile)
        self.assertTrue(os.path.isfile(new_db))

        for f in (new_db,new_configfile):
            self.assertTrue(os.path.isfile(f))
        for f in (new_db,new_configfile):
            os.remove(f)        

    

    def test_default_configs(self):
        dirname=None
        if os.getenv("HOME"):
            dirname=os.getenv("HOME")
        elif os.getenv("USERPROFILE"):
            dirname=os.getenv("HOME")
        self.assertTrue(fattybugs._default_configfile(),os.path.join(dirname,".fattybugs"))        
                        

    def test_bug_details(self):
        newid=self._insert_data()    

        return_struct=self.BugDB.bug_data(bug_id=newid)
        inserted=self._default_insert_data()        

        return_struct_subset={k:return_struct[k] for k in inserted}
        inserted["date"]=datetime.date.today()
        return_struct_subset["date"]=return_struct[self.BugDB.CREATED_DATE_COLUMN].date()

        self.assertTrue(inserted,return_struct_subset)
        

    def _insert_data(self,input_data=None):
        if not input_data:
            input_data=self._default_insert_data()

        lastrowid=self.BugDB.new_bug(**input_data)

        return lastrowid

    def _default_multi_insert_data(self):

        row_one={self.BugDB.NAME_COLUMN:"test_bug_one",
              self.BugDB.XB_COLUMN:"dont suck at all",
              self.BugDB.OB_COLUMN:"totally sucks, completely",
              self.BugDB.ASS_COLUMN:"sucker #2",
              self.BugDB.STEPS_COLUMN:"1. Open program\n2. Do something"}
        row_two=  {self.BugDB.NAME_COLUMN:"test_bug_lostcount",
            self.BugDB.XB_COLUMN:"dont suck at all",
              self.BugDB.OB_COLUMN:"totally sucks",
              self.BugDB.ASS_COLUMN:"sucker #3",
              self.BugDB.STEPS_COLUMN:"1. Open program\n2. Do anything"}        

        return [row_one,row_two]

    def _default_insert_data(self):
        
        return {self.BugDB.NAME_COLUMN:"test_bug",
              self.BugDB.XB_COLUMN:"dont suc",
              self.BugDB.OB_COLUMN:"totally sucks",
              self.BugDB.ASS_COLUMN:"sucker #1",
              self.BugDB.STEPS_COLUMN:"1. Open program\n2. Do anything"}
            
if __name__=='__main__':
    unittest.main()
