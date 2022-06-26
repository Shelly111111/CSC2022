import defaultSettings from '@/settings'

const title = defaultSettings.title || 'CSC2022'

export default function getPageTitle(pageTitle) {
  if (pageTitle) {
    return `${pageTitle} - ${title}`
  }
  return `${title}`
}
