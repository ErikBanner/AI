//
//  ViewController.swift
//  Bayesian Network
//
//  Created by MonsterHulk on 2015-10-26.
//  Copyright © 2015 MonsterHulk Inc. All rights reserved.
//

import UIKit

class ViewController: UIViewController {

    override func viewDidLoad() {
        super.viewDidLoad()
        let OC = Factor(variables: ["OC"], rows: [["T","0.6"],["F","0.4"]])
        let Fraud = Factor(variables: ["Trav","Fraud"], rows: [["T","T","0.01"],["T","F","0.99"],["F","T","0.004"],["F","F","0.996"]])
        //let Fraud = Factor(variables: ["Fraud","Trav"], rows: [["T","T","0.01"],["F","T","0.004"],["T","F","0.99"],["F","F","0.996"]])
        let Trav = Factor(variables: ["Trav"], rows: [["T","0.05"],["F","0.95"]])
        //let FP = Factor(variables: ["Trav","Fraud","FP"], rows: [["T","T","T","0.9"],["T","T","F","0.1"],["T","F","T","0.9"],["T","F","F","0.1"],["F","T","T","0.1"],["F","T","F","0.9"],["F","F","T","0.01"],["F","F","F","0.99"]])
        let FP = Factor(variables: ["FP","Trav","Fraud"], rows: [["T","T","T","0.9"],["T","T","F","0.9"],["T","F","T","0.1"],["T","F","F","0.01"],["F","T","T","0.1"],["F","T","F","0.1"],["F","F","T","0.9"],["F","F","F","0.99"]])

        let IP = Factor(variables: ["OC","Fraud","IP"], rows: [["T","T","T","0.02"],["T","T","F","0.98"],["T","F","T","0.01"],["T","F","F","0.99"],["F","T","T","0.011"],["F","T","F","0.989"],["F","F","T","0.001"],["F","F","F","0.999"]])
        let CRP = Factor(variables: ["OC","CRP"], rows: [["T","T","0.1"],["T","F","0.9"],["F","T","0.001"],["F","F","0.999"]])
        
        let factorList = [OC, Fraud, Trav, FP, IP, CRP]
        let queryVariables = ["Fraud"]
        let orderedListOfHiddenVariables = ["Trav", "FP", "Fraud", "IP", "OC", "CRP"]
        //let evidenceList = ["FP":"T", "IP":"F", "CRP":"T", "Trav":"T"]
        let evidenceList = ["":""]
        
        let answer = Factor.inference(factorList, queryVariables: queryVariables, orderedListOfHiddenVariables: orderedListOfHiddenVariables, evidenceList: evidenceList)
        print("Final factor:")
        print(answer.rows)
        print("Answer:")
        print(answer.rows[0][1])
        
//        let a = Factor(variables: ["Fraud", "Trav"], rows: [["T", "T", "0.01"],  ["F", "T", "0.004"],["T", "F", "0.99"], ["F", "F", "0.996"]])
//        let b = Factor(variables: ["Trav"], rows: [["T", "0.05"], ["F", "0.95"]])
//        let c = Factor(variables: ["Trav", "Fraud"], rows: [["T", "T", "0.9"], ["T", "F", "0.9"], ["F", "T", "0.1"], ["F", "F", "0.01"]])
//        let d = Factor.multiply(a, factor2: b)
//        let e = Factor.multiply(c, factor2: d)
//        print("=======")
//        print(d.variables)
//        print(d.rows)
//        print(e.variables)
//        print(e.rows)

    }
}

