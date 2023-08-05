Object.defineProperty(exports, "__esModule", { value: true });
exports.validateWidget = exports.deleteDashboard = exports.updateDashboard = exports.fetchDashboard = exports.createDashboard = void 0;
var indicator_1 = require("app/actionCreators/indicator");
var locale_1 = require("app/locale");
function createDashboard(api, orgId, newDashboard, duplicate) {
    var title = newDashboard.title, widgets = newDashboard.widgets;
    var promise = api.requestPromise("/organizations/" + orgId + "/dashboards/", {
        method: 'POST',
        data: { title: title, widgets: widgets, duplicate: duplicate },
    });
    promise.catch(function (response) {
        var _a;
        var errorResponse = (_a = response === null || response === void 0 ? void 0 : response.responseJSON) !== null && _a !== void 0 ? _a : null;
        if (errorResponse) {
            indicator_1.addErrorMessage(errorResponse);
        }
        else {
            indicator_1.addErrorMessage(locale_1.t('Unable to create dashboard'));
        }
    });
    return promise;
}
exports.createDashboard = createDashboard;
function fetchDashboard(api, orgId, dashboardId) {
    var promise = api.requestPromise("/organizations/" + orgId + "/dashboards/" + dashboardId + "/", {
        method: 'GET',
    });
    promise.catch(function (response) {
        var _a;
        var errorResponse = (_a = response === null || response === void 0 ? void 0 : response.responseJSON) !== null && _a !== void 0 ? _a : null;
        if (errorResponse) {
            indicator_1.addErrorMessage(errorResponse);
        }
        else {
            indicator_1.addErrorMessage(locale_1.t('Unable to load dashboard'));
        }
    });
    return promise;
}
exports.fetchDashboard = fetchDashboard;
function updateDashboard(api, orgId, dashboard) {
    var data = {
        title: dashboard.title,
        widgets: dashboard.widgets,
    };
    var promise = api.requestPromise("/organizations/" + orgId + "/dashboards/" + dashboard.id + "/", {
        method: 'PUT',
        data: data,
    });
    promise.catch(function (response) {
        var _a;
        var errorResponse = (_a = response === null || response === void 0 ? void 0 : response.responseJSON) !== null && _a !== void 0 ? _a : null;
        if (errorResponse) {
            indicator_1.addErrorMessage(errorResponse);
        }
        else {
            indicator_1.addErrorMessage(locale_1.t('Unable to update dashboard'));
        }
    });
    return promise;
}
exports.updateDashboard = updateDashboard;
function deleteDashboard(api, orgId, dashboardId) {
    var promise = api.requestPromise("/organizations/" + orgId + "/dashboards/" + dashboardId + "/", {
        method: 'DELETE',
    });
    promise.catch(function (response) {
        var _a;
        var errorResponse = (_a = response === null || response === void 0 ? void 0 : response.responseJSON) !== null && _a !== void 0 ? _a : null;
        if (errorResponse) {
            indicator_1.addErrorMessage(errorResponse);
        }
        else {
            indicator_1.addErrorMessage(locale_1.t('Unable to delete dashboard'));
        }
    });
    return promise;
}
exports.deleteDashboard = deleteDashboard;
function validateWidget(api, orgId, widget) {
    var promise = api.requestPromise("/organizations/" + orgId + "/dashboards/widgets/", {
        method: 'POST',
        data: widget,
    });
    return promise;
}
exports.validateWidget = validateWidget;
//# sourceMappingURL=dashboards.jsx.map