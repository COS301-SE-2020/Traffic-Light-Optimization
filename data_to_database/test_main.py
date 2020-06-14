import unittest
import main

class MainTest(unittest.TestCase):

    def test_readData_incorrect(self): #file path does not exist
        testPath =  r'traffic-signals-status-1.csv'
        main.readfile.setPath(testPath)
        main.readfile.readData()
        path = main.readfile.path
        self.assertNotEqual(path, main.path)

    def test_readData_correct(self): #path exists
        testPath =  r'data/traffic-signals-status-1.csv'
        main.readfile.setPath(testPath)
        main.readfile.readData()
        path = main.readfile.path
        self.assertEqual(path, main.path)

    def test_org_incorrect(self): #if org is incorrect
        testOrg = "organisation"
        main.write.writeToDB(main.bucket, testOrg)
        self.assertNotEqual(main.write.p, "correct")

    def test_bucket_incorrect(self): #if bucket is incorrect
        testBucket = "bucket"
        main.write.writeToDB(testBucket, main.organisation)
        self.assertNotEqual(main.write.p, "correct", msg = "The bucket is incorrect")

    def test_url_incorrect(self): #if url is incorrect
        testUrl = "www.google.com"
        main.initialize.connectToDB(testUrl, main.token, main.organisation)
        main.write.writeToDB(main.bucket, testUrl)
        self.assertNotEqual(main.write.p, "correct", msg = "The url is incorrect")