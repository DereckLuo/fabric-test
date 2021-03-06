# Copyright IBM Corp. All Rights Reserved.
#
# SPDX-License-Identifier: Apache-2.0
#

import unittest
import subprocess

logs_directory = '../../tools/PTE/CITest/Logs'
operator_directory = '../../tools/operator'
k8s_testsuite = '../../tools/operator/scripts'

# error messages
testScriptFailed =      "Test Failed with non-zero exit code; check for errors in fabric-test/tools/PTE/CITest"
migrationFailure =      "Error: Failed to migrate from kafka to etcdraft"
invokeFailure =         "Error: incorrect number of INVOKE transactions sent or received"
queryCountFailure =     "Error: incorrect number of QUERY transactions sent or received"


class System_Tests_Kafka_Couchdb_TLS(unittest.TestCase):

    def test_01downNetwork(self):

        # Teardown the network
        returncode = subprocess.call("./operator.sh -a down -f ../testdata/kafka-couchdb-tls-network-spec.yml", cwd=k8s_testsuite, shell=True)
        self.assertEqual(returncode, 0, msg=testScriptFailed)

    def test_02launchNetwork(self):

        # Launch the network
        returncode = subprocess.call("./operator.sh -a up -f ../testdata/kafka-couchdb-tls-network-spec.yml", cwd=k8s_testsuite, shell=True)
        self.assertEqual(returncode, 0, msg=testScriptFailed)

    def test_03createJoinChannel(self):

        returncode = subprocess.call("./operator.sh -c", cwd=k8s_testsuite, shell=True)
        self.assertEqual(returncode, 0, msg=testScriptFailed)

    def test_04installInstantiation(self):

        returncode = subprocess.call("./operator.sh -i", cwd=k8s_testsuite, shell=True)
        self.assertEqual(returncode, 0, msg=testScriptFailed)

    def test_05samplecc_orgAnchor_2chan(self):

        # Run the test scenario: Execute invokes and query tests.
        returncode = subprocess.call("./operator.sh -t samplecc_go_2chan", cwd=k8s_testsuite, shell=True)
        self.assertEqual(returncode, 0, msg=testScriptFailed)

        # check the counts
        count = subprocess.check_output(
                "grep \"CONSTANT INVOKE Overall transactions: sent 8000 received 8000\" samplecc_go_2chan_i_pteReport.txt | wc -l",
                cwd=logs_directory, shell=True)
        self.assertEqual(int(count.strip()), 1, msg=invokeFailure)

        count = subprocess.check_output(
                "grep \"CONSTANT QUERY Overall transactions: sent 8000 received 8000 failures 0\" samplecc_go_2chan_q_pteReport.txt | wc -l",
                cwd=logs_directory, shell=True)
        self.assertEqual(int(count.strip()), 1, msg=queryCountFailure)

    def test_06samplejs_orgAnchor_2chan(self):

        # Run the test scenario: Execute invokes and query tests.
        returncode = subprocess.call("./operator.sh -t samplejs_node_2chan", cwd=k8s_testsuite, shell=True)
        self.assertEqual(returncode, 0, msg=testScriptFailed)

        # check the counts
        count = subprocess.check_output(
                "grep \"CONSTANT INVOKE Overall transactions: sent 8000 received 8000\" samplejs_node_2chan_i_pteReport.txt | wc -l",
                cwd=logs_directory, shell=True)
        self.assertEqual(int(count.strip()), 1, msg=invokeFailure)

        count = subprocess.check_output(
                "grep \"CONSTANT QUERY Overall transactions: sent 8000 received 8000 failures 0\" samplejs_node_2chan_q_pteReport.txt | wc -l",
                cwd=logs_directory, shell=True)
        self.assertEqual(int(count.strip()), 1, msg=queryCountFailure)

    def test_07sbecc_go_2chan_endorse(self):

        # Run the test scenario: Execute invokes and query tests.
        returncode = subprocess.call("./operator.sh -t sbecc_go_2chan_endorse", cwd=k8s_testsuite, shell=True)
        self.assertEqual(returncode, 0, msg=testScriptFailed)

        # check the counts
        count = subprocess.check_output(
                "grep \"CONSTANT INVOKE Overall transactions: sent 8000 received 8000\" sbecc_go_2chan_endorse_i_pteReport.txt | wc -l",
                cwd=logs_directory, shell=True)
        self.assertEqual(int(count.strip()), 1, msg=invokeFailure)

    def test_08samplecc_go_8MB_TX(self):

        # Run the test scenario: Execute invokes and query tests.
        returncode = subprocess.call("./operator.sh -t samplecc_go_8MB_TX", cwd=k8s_testsuite, shell=True)
        self.assertEqual(returncode, 0, msg=testScriptFailed)

        # check the counts
        count = subprocess.check_output(
                "grep \"CONSTANT INVOKE Overall transactions: sent 40 received 40\" samplecc_go_8MB_i_pteReport.txt | wc -l",
                cwd=logs_directory, shell=True)
        self.assertEqual(int(count.strip()), 1, msg=invokeFailure)

        # migrate from kafka to etcdraft network
        # Migrate all channels specified in the networkspec file
    def test_09raftMigration(self):

        # Migrate the network from kafka to raft
        returncode = subprocess.call("./operator.sh -t migrate", cwd=k8s_testsuite, shell=True)
        self.assertEqual(returncode, 0, msg=testScriptFailed)

        # check the migration status
        count = subprocess.check_output(
                "grep \"Successfully migrated from kafka to etcdraft\" kafka-couchdb-tls-network-spec_kafka_2_raft_migrate.log | wc -l",
                cwd=logs_directory, shell=True)
        self.assertEqual(int(count.strip()), 1, msg=migrationFailure)

    # Send transactions after migrate from kafka to etcdraft network
    def test_10samplecc_orgAnchor_2chan(self):

        # Run the test scenario: Execute invokes and query tests.
        returncode = subprocess.call("./operator.sh -t samplecc_go_2chan", cwd=k8s_testsuite, shell=True)
        self.assertEqual(returncode, 0, msg=testScriptFailed)

        # check the counts
        count = subprocess.check_output(
                "grep \"CONSTANT INVOKE Overall transactions: sent 8000 received 8000\" samplecc_go_2chan_i_pteReport.txt | wc -l",
                cwd=logs_directory, shell=True)
        self.assertEqual(int(count.strip()), 1, msg=invokeFailure)

        count = subprocess.check_output(
                "grep \"CONSTANT QUERY Overall transactions: sent 8000 received 8000 failures 0\" samplecc_go_2chan_q_pteReport.txt | wc -l",
                cwd=logs_directory, shell=True)
        self.assertEqual(int(count.strip()), 1, msg=queryCountFailure)

    def test_11downNetwork(self):

        # Teardown the network
        returncode = subprocess.call("./operator.sh -a down -f ../testdata/kafka-couchdb-tls-network-spec.yml", cwd=k8s_testsuite, shell=True)
        self.assertEqual(returncode, 0, msg=testScriptFailed)

class System_Tests_Raft_Couchdb_Mutual(unittest.TestCase):

    def test_01downNetwork(self):

        # Teardown the network
        returncode = subprocess.call("./operator.sh -a down -f ../testdata/raft-couchdb-mutualtls-servdisc-network-spec.yml", cwd=k8s_testsuite, shell=True)
        self.assertEqual(returncode, 0, msg=testScriptFailed)

    def test_02launchNetwork(self):

        # Launch the network
        returncode = subprocess.call("./operator.sh -a up -f ../testdata/raft-couchdb-mutualtls-servdisc-network-spec.yml", cwd=k8s_testsuite, shell=True)
        self.assertEqual(returncode, 0, msg=testScriptFailed)

    def test_03createJoinChannel(self):

        returncode = subprocess.call("./operator.sh -c", cwd=k8s_testsuite, shell=True)
        self.assertEqual(returncode, 0, msg=testScriptFailed)

    def test_04installInstantiation(self):

        returncode = subprocess.call("./operator.sh -i", cwd=k8s_testsuite, shell=True)
        self.assertEqual(returncode, 0, msg=testScriptFailed)

    def test_05samplecc_orgAnchor_2chan(self):

        # Run the test scenario: Execute invokes and query tests.
        returncode = subprocess.call("./operator.sh -t samplecc_go_2chan", cwd=k8s_testsuite, shell=True)
        self.assertEqual(returncode, 0, msg=testScriptFailed)

        # check the counts
        count = subprocess.check_output(
                "grep \"CONSTANT INVOKE Overall transactions: sent 8000 received 8000\" samplecc_go_2chan_i_pteReport.txt | wc -l",
                cwd=logs_directory, shell=True)
        self.assertEqual(int(count.strip()), 1, msg=invokeFailure)

        count = subprocess.check_output(
                "grep \"CONSTANT QUERY Overall transactions: sent 8000 received 8000 failures 0\" samplecc_go_2chan_q_pteReport.txt | wc -l",
                cwd=logs_directory, shell=True)
        self.assertEqual(int(count.strip()), 1, msg=queryCountFailure)

    def test_06samplejs_orgAnchor_2chan(self):

        # Run the test scenario: Execute invokes and query tests.
        returncode = subprocess.call("./operator.sh -t samplejs_node_2chan", cwd=k8s_testsuite, shell=True)
        self.assertEqual(returncode, 0, msg=testScriptFailed)

        # check the counts
        count = subprocess.check_output(
                "grep \"CONSTANT INVOKE Overall transactions: sent 8000 received 8000\" samplejs_node_2chan_i_pteReport.txt | wc -l",
                cwd=logs_directory, shell=True)
        self.assertEqual(int(count.strip()), 1, msg=invokeFailure)

        count = subprocess.check_output(
                "grep \"CONSTANT QUERY Overall transactions: sent 8000 received 8000 failures 0\" samplejs_node_2chan_q_pteReport.txt | wc -l",
                cwd=logs_directory, shell=True)
        self.assertEqual(int(count.strip()), 1, msg=queryCountFailure)

    def test_07samplecc_go_8MB_TX(self):

        # Run the test scenario: Execute invokes and query tests.
        returncode = subprocess.call("./operator.sh -t samplecc_go_8MB_TX", cwd=k8s_testsuite, shell=True)
        self.assertEqual(returncode, 0, msg=testScriptFailed)

        # check the counts
        count = subprocess.check_output(
                "grep \"CONSTANT INVOKE Overall transactions: sent 40 received 40\" samplecc_go_8MB_i_pteReport.txt | wc -l",
                cwd=logs_directory, shell=True)
        self.assertEqual(int(count.strip()), 1, msg=invokeFailure)

    def test_08samplecc_go_50MB_TX(self):

        # Run the test scenario: Execute invokes and query tests.
        returncode = subprocess.call("./operator.sh -t samplecc_go_50MB_TX", cwd=k8s_testsuite, shell=True)
        self.assertEqual(returncode, 0, msg=testScriptFailed)

        # check the counts
        count = subprocess.check_output(
                "grep \"CONSTANT INVOKE Overall transactions: sent 2 received 2\" samplecc_go_50MB_i_pteReport.txt | wc -l",
                cwd=logs_directory, shell=True)
        self.assertEqual(int(count.strip()), 1, msg=invokeFailure)

    def test_09downNetwork(self):

        # Teardown the network
        returncode = subprocess.call("./operator.sh -a down -f ../testdata/raft-couchdb-mutualtls-servdisc-network-spec.yml", cwd=k8s_testsuite, shell=True)
        self.assertEqual(returncode, 0, msg=testScriptFailed)

class System_Tests_Kafka_Leveldb_NOTLS(unittest.TestCase):

    def test_01downNetwork(self):

        # Teardown the network
        returncode = subprocess.call("./operator.sh -a down -f ../testdata/kafka-leveldb-notls-network-spec.yml", cwd=k8s_testsuite, shell=True)
        self.assertEqual(returncode, 0, msg=testScriptFailed)

    def test_02launchNetwork(self):

        # Launch the network
        returncode = subprocess.call("./operator.sh -a up -f ../testdata/kafka-leveldb-notls-network-spec.yml", cwd=k8s_testsuite, shell=True)
        self.assertEqual(returncode, 0, msg=testScriptFailed)

    def test_03createJoinChannel(self):

        returncode = subprocess.call("./operator.sh -c", cwd=k8s_testsuite, shell=True)
        self.assertEqual(returncode, 0, msg=testScriptFailed)

    def test_04installInstantiation(self):

        returncode = subprocess.call("./operator.sh -i", cwd=k8s_testsuite, shell=True)
        self.assertEqual(returncode, 0, msg=testScriptFailed)

    def test_05samplecc_orgAnchor_2chan(self):

        # Run the test scenario: Execute invokes and query tests.
        returncode = subprocess.call("./operator.sh -t samplecc_go_2chan", cwd=k8s_testsuite, shell=True)
        self.assertEqual(returncode, 0, msg=testScriptFailed)

        # check the counts
        count = subprocess.check_output(
                "grep \"CONSTANT INVOKE Overall transactions: sent 8000 received 8000\" samplecc_go_2chan_i_pteReport.txt | wc -l",
                cwd=logs_directory, shell=True)
        self.assertEqual(int(count.strip()), 1, msg=invokeFailure)

        count = subprocess.check_output(
                "grep \"CONSTANT QUERY Overall transactions: sent 8000 received 8000 failures 0\" samplecc_go_2chan_q_pteReport.txt | wc -l",
                cwd=logs_directory, shell=True)
        self.assertEqual(int(count.strip()), 1, msg=queryCountFailure)

    def test_06samplejs_orgAnchor_2chan(self):

        # Run the test scenario: Execute invokes and query tests.
        returncode = subprocess.call("./operator.sh -t samplejs_node_2chan", cwd=k8s_testsuite, shell=True)
        self.assertEqual(returncode, 0, msg=testScriptFailed)

        # check the counts
        count = subprocess.check_output(
                "grep \"CONSTANT INVOKE Overall transactions: sent 8000 received 8000\" samplejs_node_2chan_i_pteReport.txt | wc -l",
                cwd=logs_directory, shell=True)
        self.assertEqual(int(count.strip()), 1, msg=invokeFailure)

        count = subprocess.check_output(
                "grep \"CONSTANT QUERY Overall transactions: sent 8000 received 8000 failures 0\" samplejs_node_2chan_q_pteReport.txt | wc -l",
                cwd=logs_directory, shell=True)
        self.assertEqual(int(count.strip()), 1, msg=queryCountFailure)

    def test_07samplecc_go_8MB_TX(self):

        # Run the test scenario: Execute invokes and query tests.
        returncode = subprocess.call("./operator.sh -t samplecc_go_8MB_TX", cwd=k8s_testsuite, shell=True)
        self.assertEqual(returncode, 0, msg=testScriptFailed)

        # check the counts
        count = subprocess.check_output(
                "grep \"CONSTANT INVOKE Overall transactions: sent 40 received 40\" samplecc_go_8MB_i_pteReport.txt | wc -l",
                cwd=logs_directory, shell=True)
        self.assertEqual(int(count.strip()), 1, msg=invokeFailure)

    def test_08samplecc_go_50MB_TX(self):

        # Run the test scenario: Execute invokes and query tests.
        returncode = subprocess.call("./operator.sh -t samplecc_go_50MB_TX", cwd=k8s_testsuite, shell=True)
        self.assertEqual(returncode, 0, msg=testScriptFailed)

        # check the counts
        count = subprocess.check_output(
                "grep \"CONSTANT INVOKE Overall transactions: sent 2 received 2\" samplecc_go_50MB_i_pteReport.txt | wc -l",
                cwd=logs_directory, shell=True)
        self.assertEqual(int(count.strip()), 1, msg=invokeFailure)

    def test_09downNetwork(self):

        # Teardown the network
        returncode = subprocess.call("./operator.sh -a down -f ../testdata/kafka-leveldb-notls-network-spec.yml", cwd=k8s_testsuite, shell=True)
        self.assertEqual(returncode, 0, msg=testScriptFailed)
