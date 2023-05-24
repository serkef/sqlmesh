import { test, expect } from '@playwright/test'

test('has title', async ({ page }) => {
  await page.goto('/editor')
  await expect(page).toHaveTitle(/SQLMesh by Tobiko/)
})

test('create and delete directory', async ({ page }) => {
  await page.goto('/editor')

  let elModelsContainer = page.getByTitle('Directory models')

  await elModelsContainer.waitFor()

  const elModels = elModelsContainer.getByTitle('models')

  await elModels.waitFor()
  await elModels.hover()

  const elModelsActionCreateDirectory = elModels.getByTitle('Create Directory')

  await elModelsActionCreateDirectory.waitFor()
  await elModelsActionCreateDirectory.click()

  elModelsContainer = page.getByTitle('Directory models')

  await elModelsContainer.waitFor()

  let elNewFolder = elModelsContainer.getByTitle(/^new_directory/)

  await elNewFolder.waitFor()
  await elNewFolder.hover()

  const elNewFolderActionRemoveDirectory =
    elNewFolder.getByTitle('Remove Directory')

  await elNewFolderActionRemoveDirectory.waitFor()
  await elNewFolderActionRemoveDirectory.click()

  const elDialogButtonYes = page
    .getByRole('button')
    .filter({ hasText: 'Yes, Remove' })

  await elDialogButtonYes.waitFor()
  await elDialogButtonYes.click()

  elNewFolder = elModelsContainer.getByTitle(/^new_directory/)

  expect(await elNewFolder.count()).toBe(0)
})
