import { instance } from '../utils/request'

import axios from 'axios'

export function sendImage(imgSrc1, imgSrc2) {
  var data = new URLSearchParams();
  data.append('img1', imgSrc1);
  data.append('img2', imgSrc2);
  return axios.post('http://localhost:8000/cdrecvImg', data)
}

export function sendImage2te(imgSrc) {
  var data = new URLSearchParams();
  data.append('img', imgSrc);
  return axios.post('http://localhost:8000/terecvImg', data)
}

export function sendImage2tc(imgSrc) {
  var data = new URLSearchParams();
  data.append('img', imgSrc);
  return axios.post('http://localhost:8000/tcrecvImg', data)
}

export function sendImage2od(imgSrc) {
  var data = new URLSearchParams();
  data.append('img', imgSrc);
  return axios.post('http://localhost:8000/odrecvImg', data)
}

export function postStorgeImage(imgSrc) {
  return instance({
    url: `/post_storage_image`,
    method: 'POST',
    data: {
      imgSrc
    }
  })
}

export function postStorge2Image(imgSrc) {
  return instance({
    url: `/post_storage_image2`,
    method: 'POST',
    data: {
      imgSrc
    }
  })
}

export function postTargetExtractionImage(imgSrc) {
  return instance({
    url: `/post_targetextraction_image`,
    method: 'POST',
    data: {
      imgSrc
    }
  })
}

export function postTerrainClassificationImage(imgSrc) {
  return instance({
    url: `/post_terrainclassification_image`,
    method: 'POST',
    data: {
      imgSrc
    }
  })
}

export function postObjectDetectionImage(imgSrc) {
  return instance({
    url: `/post_objectdetection_image`,
    method: 'POST',
    data: {
      imgSrc
    }
  })
}

export function postFindImage() {
  return instance({
    url: `/post_find_image1`,
    method: 'POST',

  })
}

export function postFind2Image() {
  return instance({
    url: `/post_find_image2`,
    method: 'POST',

  })
}

export function FindTargetExtractionImage() {
  return instance({
    url: `/find_targetextraction_image`,
    method: 'POST',

  })
}

export function FindTerrainClassificationImage() {
  return instance({
    url: `/find_terrainclassification_image`,
    method: 'POST',

  })
}

export function FindObjectDetectionImage() {
  return instance({
    url: `/find_objectdetection_image`,
    method: 'POST',

  })
}
