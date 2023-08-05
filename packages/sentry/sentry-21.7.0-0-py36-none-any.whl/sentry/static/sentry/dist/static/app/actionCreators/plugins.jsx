Object.defineProperty(exports, "__esModule", { value: true });
exports.disablePlugin = exports.enablePlugin = exports.fetchPlugins = void 0;
var tslib_1 = require("tslib");
var indicator_1 = require("app/actionCreators/indicator");
var pluginActions_1 = tslib_1.__importDefault(require("app/actions/pluginActions"));
var api_1 = require("app/api");
var locale_1 = require("app/locale");
var activeFetch = {};
// PluginsStore always exists, so api client should be independent of component lifecycle
var api = new api_1.Client();
function doUpdate(_a) {
    var orgId = _a.orgId, projectId = _a.projectId, pluginId = _a.pluginId, update = _a.update, params = tslib_1.__rest(_a, ["orgId", "projectId", "pluginId", "update"]);
    pluginActions_1.default.update(pluginId, update);
    var request = api.requestPromise("/projects/" + orgId + "/" + projectId + "/plugins/" + pluginId + "/", tslib_1.__assign({}, params));
    // This is intentionally not chained because we want the unhandled promise to be returned
    request
        .then(function () {
        pluginActions_1.default.updateSuccess(pluginId, update);
    })
        .catch(function (resp) {
        var err = resp && resp.responseJSON && typeof resp.responseJSON.detail === 'string'
            ? new Error(resp.responseJSON.detail)
            : new Error('Unable to update plugin');
        pluginActions_1.default.updateError(pluginId, update, err);
    });
    return request;
}
/**
 * Fetches list of available plugins for a project
 */
function fetchPlugins(_a, options) {
    var orgId = _a.orgId, projectId = _a.projectId;
    var path = "/projects/" + orgId + "/" + projectId + "/plugins/";
    // Make sure we throttle fetches
    if (activeFetch[path]) {
        return activeFetch[path];
    }
    pluginActions_1.default.fetchAll(options);
    var request = api.requestPromise(path, {
        method: 'GET',
        includeAllArgs: true,
    });
    activeFetch[path] = request;
    // This is intentionally not chained because we want the unhandled promise to be returned
    request
        .then(function (_a) {
        var _b = tslib_1.__read(_a, 3), data = _b[0], _ = _b[1], jqXHR = _b[2];
        pluginActions_1.default.fetchAllSuccess(data, {
            pageLinks: jqXHR && jqXHR.getResponseHeader('Link'),
        });
        return data;
    })
        .catch(function (err) {
        pluginActions_1.default.fetchAllError(err);
        throw new Error('Unable to fetch plugins');
    })
        .then(function () { return (activeFetch[path] = null); });
    return request;
}
exports.fetchPlugins = fetchPlugins;
/**
 * Enables a plugin
 */
function enablePlugin(params) {
    indicator_1.addLoadingMessage(locale_1.t('Enabling...'));
    return doUpdate(tslib_1.__assign(tslib_1.__assign({}, params), { update: { enabled: true }, method: 'POST' }))
        .then(function () { return indicator_1.addSuccessMessage(locale_1.t('Plugin was enabled')); })
        .catch(function () { return indicator_1.addErrorMessage(locale_1.t('Unable to enable plugin')); });
}
exports.enablePlugin = enablePlugin;
/**
 * Disables a plugin
 */
function disablePlugin(params) {
    indicator_1.addLoadingMessage(locale_1.t('Disabling...'));
    return doUpdate(tslib_1.__assign(tslib_1.__assign({}, params), { update: { enabled: false }, method: 'DELETE' }))
        .then(function () { return indicator_1.addSuccessMessage(locale_1.t('Plugin was disabled')); })
        .catch(function () { return indicator_1.addErrorMessage(locale_1.t('Unable to disable plugin')); });
}
exports.disablePlugin = disablePlugin;
//# sourceMappingURL=plugins.jsx.map