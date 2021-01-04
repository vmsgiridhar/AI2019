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

import Foundation
import TensorFlowLite


/// Information about a model file or labels file.
typealias FileInfo = (name: String, extension: String)

/// Information about the MobileNet model.
enum MobileNet {
  static let modelInfo: FileInfo = (name: "model", extension: "tflite")
}


/// This class handles all data preprocessing and makes calls to run inference on a given frame
/// by invoking the `Interpreter`. It then formats the inferences obtained and returns the top N
/// results for a successful inference.
class ModelDataHandler {
  
  private var interpreter: Interpreter
  
  // MARK: - Initializer
  /// A failable initializer for `ModelDataHandler`. A new instance is created if the model is successfully loaded from the app's main bundle. Default `threadCount` is 1.
  init?(modelFileInfo: FileInfo, threadCount: Int = 1) {
    let modelFilename = modelFileInfo.name
    
    // Construct the path to the model file.
    guard let modelPath = Bundle.main.path(
      forResource: modelFilename,
      ofType: modelFileInfo.extension
      ) else {
        print("Failed to load the model file with name: \(modelFilename).")
        return nil
    }
    
    // Specify the options for the `Interpreter`.
    let options = InterpreterOptions()
    
    do {
      // Create the `Interpreter`.
      interpreter = try Interpreter(modelPath: modelPath, options: options)
    } catch let error {
      print("Failed to create the interpreter with error: \(error.localizedDescription)")
      return nil
    }
    // Load the classes listed in the labels file.
    
  }
  
   // MARK: - Public Methods
  /// Copies the input data to the tensors, invokes the `Interpreter`, and process the inference results.
  func runModel(withInput input: Float) -> Float? {
    
    do {
      try interpreter.allocateTensors()
      
      var data: Float = input
      
      /// Copies input value to the tensor at inde 0
      let buffer: UnsafeMutableBufferPointer<Float> = UnsafeMutableBufferPointer(start: &data, count: 1)
      try interpreter.copy(Data(buffer: buffer), toInputAt: 0)
      
      /// Invokes the Interpreter
      try interpreter.invoke()
      
      ///Retreives results from the output tensor.
      let outputTensor = try interpreter.output(at: 0)
      
      let results: [Float32] = [Float32](unsafeData: outputTensor.data) ?? []
      
      guard let result = results.first else {
        
        return nil
      }
      
      return result
      
    }
    catch {
      
      print(error)
      return nil
    }
    
    
  }
  
  
}

// MARK: Extensions
extension Array {
  /// Creates a new array from the bytes of the given unsafe data.
  ///
  /// - Warning: The array's `Element` type must be trivial in that it can be copied bit for bit
  ///     with no indirection or reference-counting operations; otherwise, copying the raw bytes in
  ///     the `unsafeData`'s buffer to a new array returns an unsafe copy.
  /// - Note: Returns `nil` if `unsafeData.count` is not a multiple of
  ///     `MemoryLayout<Element>.stride`.
  /// - Parameter unsafeData: The data containing the bytes to turn into an array.
  init?(unsafeData: Data) {
    guard unsafeData.count % MemoryLayout<Element>.stride == 0 else { return nil }
    #if swift(>=5.0)
    self = unsafeData.withUnsafeBytes { .init($0.bindMemory(to: Element.self)) }
    #else
    self = unsafeData.withUnsafeBytes {
      .init(UnsafeBufferPointer<Element>(
        start: $0,
        count: unsafeData.count / MemoryLayout<Element>.stride
      ))
    }
    #endif  // swift(>=5.0)
  }
}
