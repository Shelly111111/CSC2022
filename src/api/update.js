import { instance } from '../utils/request'

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
