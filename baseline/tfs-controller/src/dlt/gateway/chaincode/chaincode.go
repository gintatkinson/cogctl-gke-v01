//  Copyright 2022-2025 ETSI SDG TeraFlowSDN (TFS) (https://tfs.etsi.org/)

//  Licensed under the Apache License, Version 2.0 (the "License");
//  you may not use this file except in compliance with the License.
//  You may obtain a copy of the License at

//       http://www.apache.org/licenses/LICENSE-2.0

//  Unless required by applicable law or agreed to in writing, software
//  distributed under the License is distributed on an "AS IS" BASIS,
//  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
//  See the License for the specific language governing permissions and
//  limitations under the License.

package main

import (
	"crypto/sha256"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"log"

	"github.com/hyperledger/fabric-contract-api-go/contractapi"
)

// Protobuf definitions
type Uuid struct {
	Uuid string `json:"uuid"`
}

type DltRecordId struct {
	DomainUuid Uuid   `json:"domain_uuid"`
	Type       string `json:"type"`
	RecordUuid Uuid   `json:"record_uuid"`
}

type DltRecord struct {
	RecordId DltRecordId `json:"record_id"`
	DataJson string      `json:"data_json"`
}

type SmartContract struct {
	contractapi.Contract
}

// InitLedger activates the chaincode
func (s *SmartContract) InitLedger(ctx contractapi.TransactionContextInterface) error {
	return nil
}

func (s *SmartContract) StoreRecord(ctx contractapi.TransactionContextInterface, recordId DltRecordId, dataJson string) error {

	key, err := createHashKey(recordId)
	if err != nil {
		return fmt.Errorf("failed to create hash key: %v", err)
	}

	// Check if the same record does not exist before adding it to the ledger
	exists, err := s.RecordExists(ctx, key)
	if err == nil && exists != nil {
		return fmt.Errorf("the record %s already exists", key)
	}

	// Trigger an event if the transaction is successful
	storedRecord := DltRecord{
		RecordId: recordId,
		DataJson: dataJson,
	}
	eventJson, err := json.Marshal(storedRecord)
	if err != nil {
		return fmt.Errorf("failed to marshal stored record: %v", err)
	}
	ctx.GetStub().SetEvent("StoreRecord", eventJson)

	// Store the record in the ledger
	return ctx.GetStub().PutState(key, []byte(dataJson))
}

func (s *SmartContract) RetrieveRecord(ctx contractapi.TransactionContextInterface, recordId DltRecordId) (string, error) {
	key, err := createHashKey(recordId)
	if err != nil {
		return "", fmt.Errorf("failed to create hash key: %v", err)
	}

	// Get the record from the ledger
	dataBytes, err := ctx.GetStub().GetState(key)
	if err != nil || dataBytes == nil {
		return "", fmt.Errorf("data not found for key %s", key)
	}
	return string(dataBytes), nil
}

func (s *SmartContract) UpdateRecord(ctx contractapi.TransactionContextInterface, recordId DltRecordId, dataJson string) error {
	key, err := createHashKey(recordId)
	if err != nil {
		return fmt.Errorf("failed to create hash key: %v", err)
	}

	// Check if the record exists before updating it
	_, err = s.RecordExists(ctx, key)
	if err != nil {
		return err
	}

	// Trigger an event if the transaction is successful
	eventData := DltRecord{RecordId: recordId, DataJson: dataJson}
	eventJson, err := json.Marshal(eventData)
	if err != nil {
		return fmt.Errorf("failed to marshal event data: %v", err)
	}
	ctx.GetStub().SetEvent("UpdateRecord", eventJson)

	// Update the record in the ledger
	return ctx.GetStub().PutState(key, []byte(dataJson))
}

func (s *SmartContract) DeleteRecord(ctx contractapi.TransactionContextInterface, recordId DltRecordId) error {
	key, err := createHashKey(recordId)
	if err != nil {
		return fmt.Errorf("failed to create hash key: %v", err)
	}

	// Check if the record exists before deleting it
	exists, err := s.RecordExists(ctx, key)
	if err != nil {
		return err
	}

	// Trigger an event if the transaction is successful
	eventData := DltRecord{RecordId: recordId, DataJson: string(exists)}
	eventJson, err := json.Marshal(eventData)
	if err != nil {
		return fmt.Errorf("failed to marshal event data: %v", err)
	}
	ctx.GetStub().SetEvent("DeleteRecord", eventJson)

	// Delete the record from the ledger
	return ctx.GetStub().DelState(key)
}

func (s *SmartContract) RecordExists(ctx contractapi.TransactionContextInterface, key string) ([]byte, error) {
	jsonData, err := ctx.GetStub().GetState(key)
	if err != nil {
		return nil, fmt.Errorf("failed to read from world state: %v", err)
	}
	if jsonData == nil {
		return nil, fmt.Errorf("the record %s does not exist", key)
	}
	return jsonData, nil
}

func (s *SmartContract) GetAllRecords(ctx contractapi.TransactionContextInterface) ([]map[string]interface{}, error) {
	// Range query with empty string for startKey and endKey does an
	// open-ended query of all records in the chaincode namespace.
	resultsIterator, err := ctx.GetStub().GetStateByRange("", "")
	if err != nil {
		return nil, err
	}
	defer resultsIterator.Close()

	var records []map[string]interface{}
	for resultsIterator.HasNext() {
		queryResponse, err := resultsIterator.Next()
		if err != nil {
			return nil, err
		}

		var generic map[string]interface{}
		if err := json.Unmarshal(queryResponse.Value, &generic); err != nil {
			return nil, fmt.Errorf("invalid JSON data: %v", err)
		}

		records = append(records, generic)
	}

	return records, nil
}

func createHashKey(recordId DltRecordId) (string, error) {
	recordIdJson, err := json.Marshal(recordId)
	if err != nil {
		return "", fmt.Errorf("failed to marshal record ID: %v", err)
	}

	hash := sha256.New()
	hash.Write(recordIdJson)
	return hex.EncodeToString(hash.Sum(nil)), nil
}

func main() {
	recordChaincode, err := contractapi.NewChaincode(&SmartContract{})
	if err != nil {
		log.Panicf("Error creating chaincode: %v", err)
	}

	if err := recordChaincode.Start(); err != nil {
		log.Panicf("Error starting chaincode: %v", err)
	}
}
