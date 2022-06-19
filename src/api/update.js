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

export function postStorgeImage(imgSrc) {
  return instance({
    url: `/post_storage_image`,
    method: 'POST',
    data: {
      imgSrc
    }
  })
}

export function postFindImage() {
  return instance({
    url: `/post_find_image`,
    method: 'POST',

  })
}
