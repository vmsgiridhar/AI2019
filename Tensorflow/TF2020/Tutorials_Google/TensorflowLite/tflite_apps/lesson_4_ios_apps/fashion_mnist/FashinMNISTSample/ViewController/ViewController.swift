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
  @IBOutlet weak var collectionView: UICollectionView!
  
  
  // MARK: Instance Variables
  let imageNames: [String] = ["0", "1", "2", "3", "4", "5"]
  var inferences: [String] = ["","","","","",""]
  
 
  // Handles all data preprocessing and makes calls to run inference through the `Interpreter`.
  private var modelDataHandler: ModelDataHandler? =
    ModelDataHandler(modelFileInfo: MobileNet.modelInfo, labelsFileInfo: MobileNet.labelsInfo)
  
  
  override func viewDidLoad() {
    super.viewDidLoad()
    collectionView.dataSource = self
    collectionView.delegate = self
    collectionView.reloadData()
    
    
    guard modelDataHandler != nil else {
      fatalError("Model set up failed")
    }
    
  }
  
}

// MARK: Extensions
extension ViewController: UICollectionViewDelegate, UICollectionViewDataSource {
  
  func numberOfSections(in collectionView: UICollectionView) -> Int {
    return 1
  }
  
  func collectionView(_ collectionView: UICollectionView, numberOfItemsInSection section: Int) -> Int {
    
    return imageNames.count
  }
  
  func collectionView(_ collectionView: UICollectionView, cellForItemAt indexPath: IndexPath) -> UICollectionViewCell {
    
    let cell = collectionView.dequeueReusableCell(withReuseIdentifier: "IMAGE_CELL", for: indexPath) as! ImageCell
    
    cell.imageView.image = UIImage(named: imageNames[indexPath.item])
    cell.inferenceLabel.text = inferences[indexPath.item]
    
    return cell
    
  }
  
  func collectionView(_ collectionView: UICollectionView, didSelectItemAt indexPath: IndexPath) {
    
  // Gets the grayscale pixel buffer
    guard  let image = UIImage(named: imageNames[indexPath.item]),
      let pixelBuffer = image.grayScalePixelBuffer() else {
        return
        
    }
    
    // Hands over the pixel buffer to ModelDatahandler to perform inference
    let result = modelDataHandler?.runModel(onFrame: pixelBuffer)
    
    // Formats inferences and resturns the results
    guard let inferenceResult = result?.inferences, let firstInference = inferenceResult.first else {
      return
    }
    
    inferences[indexPath.item] = firstInference.label
    collectionView.reloadData()
    
  }
  
  
  
}

