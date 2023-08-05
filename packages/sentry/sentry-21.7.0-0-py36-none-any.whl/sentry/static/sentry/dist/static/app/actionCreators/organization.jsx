Object.defineProperty(exports, "__esModule", { value: true });
exports.fetchOrganizationDetails = void 0;
var tslib_1 = require("tslib");
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var indicator_1 = require("app/actionCreators/indicator");
var organizations_1 = require("app/actionCreators/organizations");
var globalSelectionActions_1 = tslib_1.__importDefault(require("app/actions/globalSelectionActions"));
var organizationActions_1 = tslib_1.__importDefault(require("app/actions/organizationActions"));
var projectActions_1 = tslib_1.__importDefault(require("app/actions/projectActions"));
var teamActions_1 = tslib_1.__importDefault(require("app/actions/teamActions"));
var api_1 = require("app/api");
var projectsStore_1 = tslib_1.__importDefault(require("app/stores/projectsStore"));
var teamStore_1 = tslib_1.__importDefault(require("app/stores/teamStore"));
var getPreloadedData_1 = require("app/utils/getPreloadedData");
function fetchOrg(api, slug, detailed, isInitialFetch) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var detailedQueryParam, org;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    detailedQueryParam = detailed ? 1 : 0;
                    return [4 /*yield*/, getPreloadedData_1.getPreloadedDataPromise("organization?detailed=" + detailedQueryParam, slug, function () {
                            // This data should get preloaded in static/sentry/index.ejs
                            // If this url changes make sure to update the preload
                            return api.requestPromise("/organizations/" + slug + "/", {
                                query: { detailed: detailedQueryParam },
                            });
                        }, isInitialFetch)];
                case 1:
                    org = _a.sent();
                    if (!org) {
                        throw new Error('retrieved organization is falsey');
                    }
                    organizationActions_1.default.update(org, { replace: true });
                    organizations_1.setActiveOrganization(org);
                    return [2 /*return*/, org];
            }
        });
    });
}
function fetchProjectsAndTeams(slug, isInitialFetch) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var uncancelableApi, _a, projects, teams, err_1;
        return tslib_1.__generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    uncancelableApi = new api_1.Client();
                    _b.label = 1;
                case 1:
                    _b.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, Promise.all([
                            getPreloadedData_1.getPreloadedDataPromise('projects', slug, function () {
                                // This data should get preloaded in static/sentry/index.ejs
                                // If this url changes make sure to update the preload
                                return uncancelableApi.requestPromise("/organizations/" + slug + "/projects/", {
                                    query: {
                                        all_projects: 1,
                                        collapse: 'latestDeploys',
                                    },
                                });
                            }, isInitialFetch),
                            getPreloadedData_1.getPreloadedDataPromise('teams', slug, 
                            // This data should get preloaded in static/sentry/index.ejs
                            // If this url changes make sure to update the preload
                            function () { return uncancelableApi.requestPromise("/organizations/" + slug + "/teams/"); }, isInitialFetch),
                        ])];
                case 2:
                    _a = tslib_1.__read.apply(void 0, [_b.sent(), 2]), projects = _a[0], teams = _a[1];
                    return [2 /*return*/, [projects, teams]];
                case 3:
                    err_1 = _b.sent();
                    // It's possible these requests fail with a 403 if the user has a role with insufficient access
                    // to projects and teams, but *can* access org details (e.g. billing).
                    // An example of this is in org settings.
                    //
                    // Ignore 403s and bubble up other API errors
                    if (err_1.status !== 403) {
                        throw err_1;
                    }
                    return [3 /*break*/, 4];
                case 4: return [2 /*return*/, [[], []]];
            }
        });
    });
}
/**
 * Fetches an organization's details with an option for the detailed representation
 * with teams and projects
 *
 * @param api A reference to the api client
 * @param slug The organization slug
 * @param detailed Whether or not the detailed org details should be retrieved
 * @param silent Should we silently update the organization (do not clear the
 *               current organization in the store)
 */
function fetchOrganizationDetails(api, slug, detailed, silent, isInitialFetch) {
    var _a, _b, _c, _d, _e;
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var promises, _f, org, projectsAndTeams, _g, projects, teams, err_2, errMessage;
        return tslib_1.__generator(this, function (_h) {
            switch (_h.label) {
                case 0:
                    if (!silent) {
                        organizationActions_1.default.fetchOrg();
                        projectActions_1.default.reset();
                        globalSelectionActions_1.default.reset();
                    }
                    _h.label = 1;
                case 1:
                    _h.trys.push([1, 3, , 4]);
                    promises = [fetchOrg(api, slug, detailed, isInitialFetch)];
                    if (!detailed) {
                        promises.push(fetchProjectsAndTeams(slug, isInitialFetch));
                    }
                    return [4 /*yield*/, Promise.all(promises)];
                case 2:
                    _f = tslib_1.__read.apply(void 0, [_h.sent(), 2]), org = _f[0], projectsAndTeams = _f[1];
                    if (!detailed) {
                        _g = tslib_1.__read(projectsAndTeams, 2), projects = _g[0], teams = _g[1];
                        projectActions_1.default.loadProjects(projects);
                        teamActions_1.default.loadTeams(teams);
                    }
                    if (org && detailed) {
                        // TODO(davidenwang): Change these to actions after organization.projects
                        // and organization.teams no longer exists. Currently if they were changed
                        // to actions it would cause OrganizationContext to rerender many times
                        teamStore_1.default.loadInitialData(org.teams);
                        projectsStore_1.default.loadInitialData(org.projects);
                    }
                    return [3 /*break*/, 4];
                case 3:
                    err_2 = _h.sent();
                    if (!err_2) {
                        return [2 /*return*/];
                    }
                    organizationActions_1.default.fetchOrgError(err_2);
                    if (err_2.status === 403 || err_2.status === 401) {
                        errMessage = typeof ((_a = err_2.responseJSON) === null || _a === void 0 ? void 0 : _a.detail) === 'string'
                            ? (_b = err_2.responseJSON) === null || _b === void 0 ? void 0 : _b.detail
                            : typeof ((_d = (_c = err_2.responseJSON) === null || _c === void 0 ? void 0 : _c.detail) === null || _d === void 0 ? void 0 : _d.message) === 'string'
                                ? (_e = err_2.responseJSON) === null || _e === void 0 ? void 0 : _e.detail.message
                                : null;
                        if (errMessage) {
                            indicator_1.addErrorMessage(errMessage);
                        }
                        return [2 /*return*/];
                    }
                    Sentry.captureException(err_2);
                    return [3 /*break*/, 4];
                case 4: return [2 /*return*/];
            }
        });
    });
}
exports.fetchOrganizationDetails = fetchOrganizationDetails;
//# sourceMappingURL=organization.jsx.map