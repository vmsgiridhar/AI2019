// Copyright 2019 The TensorFlow Authors. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//    http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import UIKit

class ViewController: UIViewController {
  
  // MARK: Storyboards Connections
  @IBOutlet weak var resultLabel: UILabel!
  @IBOutlet weak var inputField: UITextField!
  
  // MARK: Instance Variables
  // Handles all data preprocessing and makes calls to run inference through the `Interpreter`.
  private var modelDataHandler: ModelDataHandler? =
    ModelDataHandler(modelFileInfo: MobileNet.modelInfo)
  
  override func viewDidLoad() {
    super.viewDidLoad()
    
    guard modelDataHandler != nil else {
      fatalError("Model set up failed")
    }
    
    // Do any additional setup after loading the view, typically from a nib.
  }
  
  
  /// Performs inference on the text in input field once a text change event is
  ///trigerred
  @IBAction func inputFieldDidChangeValue(_ sender: Any) {
    
    runInference()
    
  }
  
  //MARK: Private Functions
  ///Performs inference by invoking methods from ModelDataHandler
  private func runInference() {
    
    guard let text = inputField.text, text.count > 0 else {
      resultLabel.text = "0.00"
      return
    }
    
    guard let value = Float(text) else {
      
      return
    }
    
    
    
    guard let result = self.modelDataHandler?.runModel(withInput: value) else {
      return
    }
    
    resultLabel.text = String(format: "%.2f", result)
  }
  
}

//MARK: Extensions
extension ViewController: UITextFieldDelegate {
  
  func textFieldShouldReturn(_ textField: UITextField) -> Bool {
    
    return true
  }
}

