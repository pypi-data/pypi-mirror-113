Object.defineProperty(exports, "__esModule", { value: true });
exports.fetchOrganizationDetails = exports.fetchOrganizationByMember = exports.updateOrganization = exports.changeOrganizationSlug = exports.setActiveOrganization = exports.removeAndRedirectToRemainingOrganization = exports.switchOrganization = exports.remove = exports.redirectToRemainingOrganization = void 0;
var tslib_1 = require("tslib");
var react_router_1 = require("react-router");
var globalSelection_1 = require("app/actionCreators/globalSelection");
var indicator_1 = require("app/actionCreators/indicator");
var organizationActions_1 = tslib_1.__importDefault(require("app/actions/organizationActions"));
var organizationsActions_1 = tslib_1.__importDefault(require("app/actions/organizationsActions"));
var api_1 = require("app/api");
var organizationsStore_1 = tslib_1.__importDefault(require("app/stores/organizationsStore"));
var projectsStore_1 = tslib_1.__importDefault(require("app/stores/projectsStore"));
var teamStore_1 = tslib_1.__importDefault(require("app/stores/teamStore"));
/**
 * After removing an organization, this will redirect to a remaining active organization or
 * the screen to create a new organization.
 *
 * Can optionally remove organization from organizations store.
 */
function redirectToRemainingOrganization(_a) {
    var orgId = _a.orgId, removeOrg = _a.removeOrg;
    // Remove queued, should redirect
    var allOrgs = organizationsStore_1.default.getAll().filter(function (org) { return org.status.id === 'active' && org.slug !== orgId; });
    if (!allOrgs.length) {
        react_router_1.browserHistory.push('/organizations/new/');
        return;
    }
    // Let's be smart and select the best org to redirect to
    var firstRemainingOrg = allOrgs[0];
    react_router_1.browserHistory.push("/" + firstRemainingOrg.slug + "/");
    // Remove org from SidebarDropdown
    if (removeOrg) {
        organizationsStore_1.default.remove(orgId);
    }
}
exports.redirectToRemainingOrganization = redirectToRemainingOrganization;
function remove(api, _a) {
    var successMessage = _a.successMessage, errorMessage = _a.errorMessage, orgId = _a.orgId;
    var endpoint = "/organizations/" + orgId + "/";
    return api
        .requestPromise(endpoint, {
        method: 'DELETE',
    })
        .then(function () {
        organizationsActions_1.default.removeSuccess(orgId);
        if (successMessage) {
            indicator_1.addSuccessMessage(successMessage);
        }
    })
        .catch(function () {
        organizationsActions_1.default.removeError();
        if (errorMessage) {
            indicator_1.addErrorMessage(errorMessage);
        }
    });
}
exports.remove = remove;
function switchOrganization() {
    globalSelection_1.resetGlobalSelection();
}
exports.switchOrganization = switchOrganization;
function removeAndRedirectToRemainingOrganization(api, params) {
    remove(api, params).then(function () { return redirectToRemainingOrganization(params); });
}
exports.removeAndRedirectToRemainingOrganization = removeAndRedirectToRemainingOrganization;
/**
 * Set active organization
 */
function setActiveOrganization(org) {
    organizationsActions_1.default.setActive(org);
}
exports.setActiveOrganization = setActiveOrganization;
function changeOrganizationSlug(prev, next) {
    organizationsActions_1.default.changeSlug(prev, next);
}
exports.changeOrganizationSlug = changeOrganizationSlug;
/**
 * Updates an organization for the store
 *
 * Accepts a partial organization as it will merge will existing organization
 */
function updateOrganization(org) {
    organizationsActions_1.default.update(org);
    organizationActions_1.default.update(org);
}
exports.updateOrganization = updateOrganization;
function fetchOrganizationByMember(memberId, _a) {
    var addOrg = _a.addOrg, fetchOrgDetails = _a.fetchOrgDetails;
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var api, data, org;
        return tslib_1.__generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    api = new api_1.Client();
                    return [4 /*yield*/, api.requestPromise("/organizations/?query=member_id:" + memberId)];
                case 1:
                    data = _b.sent();
                    if (!data.length) {
                        return [2 /*return*/, null];
                    }
                    org = data[0];
                    if (addOrg) {
                        // add org to SwitchOrganization dropdown
                        organizationsStore_1.default.add(org);
                    }
                    if (!fetchOrgDetails) return [3 /*break*/, 3];
                    // load SidebarDropdown with org details including `access`
                    return [4 /*yield*/, fetchOrganizationDetails(org.slug, { setActive: true, loadProjects: true })];
                case 2:
                    // load SidebarDropdown with org details including `access`
                    _b.sent();
                    _b.label = 3;
                case 3: return [2 /*return*/, org];
            }
        });
    });
}
exports.fetchOrganizationByMember = fetchOrganizationByMember;
function fetchOrganizationDetails(orgId, _a) {
    var setActive = _a.setActive, loadProjects = _a.loadProjects, loadTeam = _a.loadTeam;
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var api, data;
        return tslib_1.__generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    api = new api_1.Client();
                    return [4 /*yield*/, api.requestPromise("/organizations/" + orgId + "/")];
                case 1:
                    data = _b.sent();
                    if (setActive) {
                        setActiveOrganization(data);
                    }
                    if (loadTeam) {
                        teamStore_1.default.loadInitialData(data.teams);
                    }
                    if (loadProjects) {
                        projectsStore_1.default.loadInitialData(data.projects || []);
                    }
                    return [2 /*return*/, data];
            }
        });
    });
}
exports.fetchOrganizationDetails = fetchOrganizationDetails;
//# sourceMappingURL=organizations.jsx.map