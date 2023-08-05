Object.defineProperty(exports, "__esModule", { value: true });
exports.addRepository = exports.migrateRepository = exports.cancelDeleteRepository = exports.deleteRepository = exports.addIntegrationToProject = exports.removeIntegrationFromProject = void 0;
var indicator_1 = require("app/actionCreators/indicator");
var api_1 = require("app/api");
var locale_1 = require("app/locale");
var api = new api_1.Client();
/**
 * Removes an integration from a project.
 *
 * @param {String} orgId Organization Slug
 * @param {String} projectId Project Slug
 * @param {Object} integration The organization integration to remove
 */
function removeIntegrationFromProject(orgId, projectId, integration) {
    var endpoint = "/projects/" + orgId + "/" + projectId + "/integrations/" + integration.id + "/";
    indicator_1.addLoadingMessage();
    return api.requestPromise(endpoint, { method: 'DELETE' }).then(function () {
        indicator_1.addSuccessMessage(locale_1.t('Disabled %s for %s', integration.name, projectId));
    }, function () {
        indicator_1.addErrorMessage(locale_1.t('Failed to disable %s for %s', integration.name, projectId));
    });
}
exports.removeIntegrationFromProject = removeIntegrationFromProject;
/**
 * Add an integration to a project
 *
 * @param {String} orgId Organization Slug
 * @param {String} projectId Project Slug
 * @param {Object} integration The organization integration to add
 */
function addIntegrationToProject(orgId, projectId, integration) {
    var endpoint = "/projects/" + orgId + "/" + projectId + "/integrations/" + integration.id + "/";
    indicator_1.addLoadingMessage();
    return api.requestPromise(endpoint, { method: 'PUT' }).then(function () {
        indicator_1.addSuccessMessage(locale_1.t('Enabled %s for %s', integration.name, projectId));
    }, function () {
        indicator_1.addErrorMessage(locale_1.t('Failed to enabled %s for %s', integration.name, projectId));
    });
}
exports.addIntegrationToProject = addIntegrationToProject;
/**
 * Delete a respository
 *
 * @param {Object} client ApiClient
 * @param {String} orgId Organization Slug
 * @param {String} repositoryId Repository ID
 */
function deleteRepository(client, orgId, repositoryId) {
    indicator_1.addLoadingMessage();
    var promise = client.requestPromise("/organizations/" + orgId + "/repos/" + repositoryId + "/", {
        method: 'DELETE',
    });
    promise.then(function () { return indicator_1.clearIndicators(); }, function () { return indicator_1.addErrorMessage(locale_1.t('Unable to delete repository.')); });
    return promise;
}
exports.deleteRepository = deleteRepository;
/**
 * Cancel the deletion of a respository
 *
 * @param {Object} client ApiClient
 * @param {String} orgId Organization Slug
 * @param {String} repositoryId Repository ID
 */
function cancelDeleteRepository(client, orgId, repositoryId) {
    indicator_1.addLoadingMessage();
    var promise = client.requestPromise("/organizations/" + orgId + "/repos/" + repositoryId + "/", {
        method: 'PUT',
        data: { status: 'visible' },
    });
    promise.then(function () { return indicator_1.clearIndicators(); }, function () { return indicator_1.addErrorMessage(locale_1.t('Unable to cancel deletion.')); });
    return promise;
}
exports.cancelDeleteRepository = cancelDeleteRepository;
function applyRepositoryAddComplete(promise) {
    promise.then(function (repo) {
        var message = locale_1.tct('[repo] has been successfully added.', {
            repo: repo.name,
        });
        indicator_1.addSuccessMessage(message);
    }, function (errorData) {
        var text = errorData.responseJSON.errors
            ? errorData.responseJSON.errors.__all__
            : locale_1.t('Unable to add repository.');
        indicator_1.addErrorMessage(text);
    });
    return promise;
}
/**
 * Migrate a repository to a new integration.
 *
 * @param {Object} client ApiClient
 * @param {String} orgId Organization Slug
 * @param {String} repositoryId Repository ID
 * @param {Object} integration Integration provider data.
 */
function migrateRepository(client, orgId, repositoryId, integration) {
    var data = { integrationId: integration.id };
    indicator_1.addLoadingMessage();
    var promise = client.requestPromise("/organizations/" + orgId + "/repos/" + repositoryId + "/", {
        data: data,
        method: 'PUT',
    });
    return applyRepositoryAddComplete(promise);
}
exports.migrateRepository = migrateRepository;
/**
 * Add a repository
 *
 * @param {Object} client ApiClient
 * @param {String} orgId Organization Slug
 * @param {String} name Repository identifier/name to add
 * @param {Object} integration Integration provider data.
 */
function addRepository(client, orgId, name, integration) {
    var data = {
        installation: integration.id,
        identifier: name,
        provider: "integrations:" + integration.provider.key,
    };
    indicator_1.addLoadingMessage();
    var promise = client.requestPromise("/organizations/" + orgId + "/repos/", {
        method: 'POST',
        data: data,
    });
    return applyRepositoryAddComplete(promise);
}
exports.addRepository = addRepository;
//# sourceMappingURL=integrations.jsx.map