//
//  Model.swift
//  Bayesian Network
//
//  Created by MonsterHulk on 2015-10-26.
//  Copyright © 2015 MonsterHulk Inc. All rights reserved.
//

import Foundation
import UIKit

class Factor {
    var variables = [String]()
    var varToIndex = [String:Int]()
    var rows: [[String]]
    init(variables: [String], rows:[[String]]){
        for index in 0..<variables.count {
            varToIndex[variables[index]] = index
        }
        self.variables = variables
        self.rows = rows
    }
    
    static func restrict(factor: Factor, variable: String, value: String) -> Factor {
        var newVariables = [String]()
        var newRows = [[String]]()
        for key in factor.variables {
            if key != variable {
                newVariables.append(key)
            }
        }
        for row in factor.rows {
            if row[factor.varToIndex[variable]!] == value {
                var newRow = [String]()
                for index in 0..<row.count {
                    if index != factor.varToIndex[variable] {
                        newRow.append(row[index])
                    }
                }
                newRows.append(newRow)
            }
        }
        return Factor(variables: newVariables, rows: newRows)
    }
    
    static func multiply(factor1: Factor, factor2: Factor) -> Factor {
        var newVariables = [String]()
        var newRows = [[String]]()
        var commonVariablesDict = [String:String]()
        var commonVariables = [String]()
        
        for key in factor1.variables {
            if factor2.variables.contains(key) {
                commonVariables.append(key)
            }
        }
        
        for temp in factor1.variables {
            if !commonVariables.contains(temp) {
                newVariables.append(temp)
            }
        }
        for temp in factor2.variables {
            if !commonVariables.contains(temp) {
                newVariables.append(temp)
            }
        }
        for commonVariable in commonVariables {
            newVariables.append(commonVariable)
        }
        
        let rowLength1 = factor1.rows[0].count
        var newRow = [String]()
        for row1 in factor1.rows {
            for index in 0..<rowLength1-1 {
                let variable1 = factor1.variables[index]
                if commonVariables.contains(variable1) {
                    commonVariablesDict[variable1] = row1[index]
                }
                else {
                    newRow.append(row1[index])
                }
            }
            let val1 = Double(row1[rowLength1-1])!
            
            let copyRow = newRow
            let rowLength2 = factor2.rows[0].count
            outer: for row2 in factor2.rows {
                for index in 0..<rowLength2-1 {
                    let variable2 = factor2.variables[index]
                    if commonVariables.contains(variable2) {
                        if commonVariablesDict[variable2] != row2[index] {
                            newRow = copyRow
                            continue outer
                        }
                    }
                    else {
                        newRow.append(row2[index])
                    }
                }
                for variable3 in commonVariables {
                    newRow.append(commonVariablesDict[variable3]!)
                }
                let val2 = Double(row2[rowLength2-1])!
                newRow.append(String(val1*val2))
                newRows.append(newRow)
                newRow = copyRow
            }
            newRow.removeAll()
        }
        return Factor(variables: newVariables, rows: newRows)
    }
    
    static func sumout(factor: Factor, variable: String) -> Factor {
        var newVariables = [String]()
        var newRows = [[String]]()
        
        var values = [String]()
        for row in factor.rows {
            let index = factor.varToIndex[variable]!
            if !values.contains(row[index]) {
                values.append(row[index])
            }
        }
        var newRow = [String]()
        var restrictedFactors = [Factor]()
        for value in values {
            restrictedFactors.append(Factor.restrict(factor, variable: variable, value: value))
        }
        newVariables = restrictedFactors[0].variables
        
        let firstFactor = restrictedFactors[0]
        for row1 in firstFactor.rows {
            var modifiedRow1 = row1
            let value1 = Double(modifiedRow1.last!)!
            modifiedRow1.removeLast()
            for index in 1..<restrictedFactors.count {
                for row2 in restrictedFactors[index].rows {
                    var modifiedRow2 = row2
                    let value2 = Double(modifiedRow2.last!)!
                    modifiedRow2.removeLast()
                    if modifiedRow1 == modifiedRow2 {
                        newRow = modifiedRow2
                        newRow.append(String(value1+value2))
                        newRows.append(newRow)
                        newRow = [String]()
                    }
                }
            }
        }
        return Factor(variables: newVariables, rows: newRows)
    }
    
    static func normalize(factor: Factor) -> Factor {
        let newVariables = factor.variables
        var newRows = [[String]]()
        var sum = 0.0
        for row in factor.rows {
            sum += Double(row.last!)!
        }
        var newRow = [String]()
        for row in factor.rows {
            newRow = row
            newRow.removeLast()
            newRow.append(String(Double(row.last!)! / sum))
            newRows.append(newRow)
        }
        return Factor(variables: newVariables, rows: newRows)
    }
    
    static func inference(factorList: [Factor], queryVariables: [String], orderedListOfHiddenVariables: [String], evidenceList: [String:String]) -> Factor {
        var restrictedFactorList = [Factor]()
        print("restricted factors:")
        for factor in factorList {
            var newFactor = factor
            for key in evidenceList.keys {
                if newFactor.variables.contains(key) {
                    newFactor = Factor.restrict(newFactor, variable: key, value: evidenceList[key]!)
                }
            }
            restrictedFactorList.append(newFactor)
            print(newFactor.variables)
            print(newFactor.rows)
        }
        
        var newFactorList = restrictedFactorList
        for hiddenVariable in orderedListOfHiddenVariables {
            restrictedFactorList = newFactorList
            if !evidenceList.keys.contains(hiddenVariable) && !queryVariables.contains(hiddenVariable) {
                print("Eliminating: " + hiddenVariable)
                newFactorList.removeAll()
                var factorsToBeMultiplied = [Factor]()
                var index = 0
                print("Multiplying:")
                for factor in restrictedFactorList {
                    if factor.variables.contains(hiddenVariable) {
                        factorsToBeMultiplied.append(factor)
                        print(factor.variables)
                        print(factor.rows)
                    }
                    else {
                        newFactorList.append(factor)
                    }
                    index++
                }
                while factorsToBeMultiplied.count > 1 {
                    let first = factorsToBeMultiplied[0]
                    let second = factorsToBeMultiplied[1]
                    factorsToBeMultiplied.removeFirst()
                    factorsToBeMultiplied.removeFirst()
                    let product = Factor.multiply(first, factor2: second)
                    factorsToBeMultiplied.append(product)
                }
                print("Product:")
                print(factorsToBeMultiplied[0].variables)
                print(factorsToBeMultiplied[0].rows)
                print("Sumout:")
                let sumoutFactor = Factor.sumout(factorsToBeMultiplied[0], variable: hiddenVariable)
                print(sumoutFactor.variables)
                print(sumoutFactor.rows)
                if factorsToBeMultiplied.count != 0 {
                    newFactorList.append(sumoutFactor)
                }
            }
        }
        
        print("resulting factorList: " + String(newFactorList.count))
        for i in 0..<newFactorList.count {
            print(newFactorList[i].variables)
            print(newFactorList[i].rows)
        }
        while newFactorList.count > 1 {
            let first = newFactorList[0]
            let second = newFactorList[1]
            newFactorList.removeFirst()
            newFactorList.removeFirst()
            let product = Factor.multiply(first, factor2: second)
            newFactorList.append(product)
        }
        return Factor.normalize(newFactorList[0])
    }
}