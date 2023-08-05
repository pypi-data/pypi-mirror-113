Object.defineProperty(exports, "__esModule", { value: true });
exports.fetchAnyReleaseExistence = exports.fetchProjectsCount = exports.loadDocs = exports.createProject = exports.sendSampleEvent = exports.changeProjectSlug = exports.removeTeamFromProject = exports.addTeamToProject = exports.transferProject = exports.removeProject = exports.setActiveProject = exports.loadStatsForProject = exports._debouncedLoadStats = exports.loadStats = exports.update = void 0;
var tslib_1 = require("tslib");
var chunk_1 = tslib_1.__importDefault(require("lodash/chunk"));
var debounce_1 = tslib_1.__importDefault(require("lodash/debounce"));
var indicator_1 = require("app/actionCreators/indicator");
var projectActions_1 = tslib_1.__importDefault(require("app/actions/projectActions"));
var locale_1 = require("app/locale");
var projectsStatsStore_1 = tslib_1.__importDefault(require("app/stores/projectsStatsStore"));
function update(api, params) {
    projectActions_1.default.update(params.projectId, params.data);
    var endpoint = "/projects/" + params.orgId + "/" + params.projectId + "/";
    return api
        .requestPromise(endpoint, {
        method: 'PUT',
        data: params.data,
    })
        .then(function (data) {
        projectActions_1.default.updateSuccess(data);
        return data;
    }, function (err) {
        projectActions_1.default.updateError(err, params.projectId);
        throw err;
    });
}
exports.update = update;
function loadStats(api, params) {
    projectActions_1.default.loadStats(params.orgId, params.data);
    var endpoint = "/organizations/" + params.orgId + "/stats/";
    api.request(endpoint, {
        query: params.query,
        success: function (data) {
            projectActions_1.default.loadStatsSuccess(data);
        },
        error: function (data) {
            projectActions_1.default.loadStatsError(data);
        },
    });
}
exports.loadStats = loadStats;
// This is going to queue up a list of project ids we need to fetch stats for
// Will be cleared when debounced function fires
var _projectStatsToFetch = new Set();
// Max projects to query at a time, otherwise if we fetch too many in the same request
// it can timeout
var MAX_PROJECTS_TO_FETCH = 10;
var _queryForStats = function (api, projects, orgId, additionalQuery) {
    var idQueryParams = projects.map(function (project) { return "id:" + project; }).join(' ');
    var endpoint = "/organizations/" + orgId + "/projects/";
    var query = tslib_1.__assign({ statsPeriod: '24h', query: idQueryParams }, additionalQuery);
    return api.requestPromise(endpoint, {
        query: query,
    });
};
exports._debouncedLoadStats = debounce_1.default(function (api, projectSet, params) {
    var storedProjects = projectsStatsStore_1.default.getAll();
    var existingProjectStats = Object.values(storedProjects).map(function (_a) {
        var id = _a.id;
        return id;
    });
    var projects = Array.from(projectSet).filter(function (project) { return !existingProjectStats.includes(project); });
    if (!projects.length) {
        _projectStatsToFetch.clear();
        return;
    }
    // Split projects into more manageable chunks to query, otherwise we can
    // potentially face server timeouts
    var queries = chunk_1.default(projects, MAX_PROJECTS_TO_FETCH).map(function (chunkedProjects) {
        return _queryForStats(api, chunkedProjects, params.orgId, params.query);
    });
    Promise.all(queries)
        .then(function (results) {
        projectActions_1.default.loadStatsForProjectSuccess(results.reduce(function (acc, result) { return acc.concat(result); }, []));
    })
        .catch(function () {
        indicator_1.addErrorMessage(locale_1.t('Unable to fetch all project stats'));
    });
    // Reset projects list
    _projectStatsToFetch.clear();
}, 50);
function loadStatsForProject(api, project, params) {
    // Queue up a list of projects that we need stats for
    // and call a debounced function to fetch stats for list of projects
    _projectStatsToFetch.add(project);
    exports._debouncedLoadStats(api, _projectStatsToFetch, params);
}
exports.loadStatsForProject = loadStatsForProject;
function setActiveProject(project) {
    projectActions_1.default.setActive(project);
}
exports.setActiveProject = setActiveProject;
function removeProject(api, orgId, project) {
    var endpoint = "/projects/" + orgId + "/" + project.slug + "/";
    projectActions_1.default.removeProject(project);
    return api
        .requestPromise(endpoint, {
        method: 'DELETE',
    })
        .then(function () {
        projectActions_1.default.removeProjectSuccess(project);
        indicator_1.addSuccessMessage(locale_1.tct('[project] was successfully removed', { project: project.slug }));
    }, function (err) {
        projectActions_1.default.removeProjectError(project);
        indicator_1.addErrorMessage(locale_1.tct('Error removing [project]', { project: project.slug }));
        throw err;
    });
}
exports.removeProject = removeProject;
function transferProject(api, orgId, project, email) {
    var endpoint = "/projects/" + orgId + "/" + project.slug + "/transfer/";
    return api
        .requestPromise(endpoint, {
        method: 'POST',
        data: {
            email: email,
        },
    })
        .then(function () {
        indicator_1.addSuccessMessage(locale_1.tct('A request was sent to move [project] to a different organization', {
            project: project.slug,
        }));
    }, function (err) {
        var _a;
        var message = '';
        // Handle errors with known failures
        if (err.status >= 400 && err.status < 500 && err.responseJSON) {
            message = (_a = err.responseJSON) === null || _a === void 0 ? void 0 : _a.detail;
        }
        if (message) {
            indicator_1.addErrorMessage(locale_1.tct('Error transferring [project]. [message]', {
                project: project.slug,
                message: message,
            }));
        }
        else {
            indicator_1.addErrorMessage(locale_1.tct('Error transferring [project]', {
                project: project.slug,
            }));
        }
        throw err;
    });
}
exports.transferProject = transferProject;
/**
 * Associate a team with a project
 */
/**
 *  Adds a team to a project
 *
 * @param api API Client
 * @param orgSlug Organization Slug
 * @param projectSlug Project Slug
 * @param team Team data object
 */
function addTeamToProject(api, orgSlug, projectSlug, team) {
    var endpoint = "/projects/" + orgSlug + "/" + projectSlug + "/teams/" + team.slug + "/";
    indicator_1.addLoadingMessage();
    projectActions_1.default.addTeam(team);
    return api
        .requestPromise(endpoint, {
        method: 'POST',
    })
        .then(function (project) {
        indicator_1.addSuccessMessage(locale_1.tct('[team] has been added to the [project] project', {
            team: "#" + team.slug,
            project: projectSlug,
        }));
        projectActions_1.default.addTeamSuccess(team, projectSlug);
        projectActions_1.default.updateSuccess(project);
    }, function (err) {
        indicator_1.addErrorMessage(locale_1.tct('Unable to add [team] to the [project] project', {
            team: "#" + team.slug,
            project: projectSlug,
        }));
        projectActions_1.default.addTeamError();
        throw err;
    });
}
exports.addTeamToProject = addTeamToProject;
/**
 * Removes a team from a project
 *
 * @param api API Client
 * @param orgSlug Organization Slug
 * @param projectSlug Project Slug
 * @param teamSlug Team Slug
 */
function removeTeamFromProject(api, orgSlug, projectSlug, teamSlug) {
    var endpoint = "/projects/" + orgSlug + "/" + projectSlug + "/teams/" + teamSlug + "/";
    indicator_1.addLoadingMessage();
    projectActions_1.default.removeTeam(teamSlug);
    return api
        .requestPromise(endpoint, {
        method: 'DELETE',
    })
        .then(function (project) {
        indicator_1.addSuccessMessage(locale_1.tct('[team] has been removed from the [project] project', {
            team: "#" + teamSlug,
            project: projectSlug,
        }));
        projectActions_1.default.removeTeamSuccess(teamSlug, projectSlug);
        projectActions_1.default.updateSuccess(project);
    }, function (err) {
        indicator_1.addErrorMessage(locale_1.tct('Unable to remove [team] from the [project] project', {
            team: "#" + teamSlug,
            project: projectSlug,
        }));
        projectActions_1.default.removeTeamError(err);
        throw err;
    });
}
exports.removeTeamFromProject = removeTeamFromProject;
/**
 * Change a project's slug
 *
 * @param prev Previous slug
 * @param next New slug
 */
function changeProjectSlug(prev, next) {
    projectActions_1.default.changeSlug(prev, next);
}
exports.changeProjectSlug = changeProjectSlug;
/**
 * Send a sample event
 *
 * @param api API Client
 * @param orgSlug Organization Slug
 * @param projectSlug Project Slug
 */
function sendSampleEvent(api, orgSlug, projectSlug) {
    var endpoint = "/projects/" + orgSlug + "/" + projectSlug + "/create-sample/";
    return api.requestPromise(endpoint, {
        method: 'POST',
    });
}
exports.sendSampleEvent = sendSampleEvent;
/**
 * Creates a project
 *
 * @param api API Client
 * @param orgSlug Organization Slug
 * @param team The team slug to assign the project to
 * @param name Name of the project
 * @param platform The platform key of the project
 * @param options Additional options such as creating default alert rules
 */
function createProject(api, orgSlug, team, name, platform, options) {
    if (options === void 0) { options = {}; }
    return api.requestPromise("/teams/" + orgSlug + "/" + team + "/projects/", {
        method: 'POST',
        data: { name: name, platform: platform, default_rules: options.defaultRules },
    });
}
exports.createProject = createProject;
/**
 * Load platform documentation specific to the project. The DSN and various
 * other project specific secrets will be included in the documentation.
 *
 * @param api API Client
 * @param orgSlug Organization Slug
 * @param projectSlug Project Slug
 * @param platform Project platform.
 */
function loadDocs(api, orgSlug, projectSlug, platform) {
    return api.requestPromise("/projects/" + orgSlug + "/" + projectSlug + "/docs/" + platform + "/");
}
exports.loadDocs = loadDocs;
/**
 * Load the counts of my projects and all projects for the current user
 *
 * @param api API Client
 * @param orgSlug Organization Slug
 */
function fetchProjectsCount(api, orgSlug) {
    return api.requestPromise("/organizations/" + orgSlug + "/projects-count/");
}
exports.fetchProjectsCount = fetchProjectsCount;
/**
 * Check if there are any releases in the last 90 days.
 * Used for checking if project is using releases.
 *
 * @param api API Client
 * @param orgSlug Organization Slug
 * @param projectId Project Id
 */
function fetchAnyReleaseExistence(api, orgSlug, projectId) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var data;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, api.requestPromise("/organizations/" + orgSlug + "/releases/stats/", {
                        method: 'GET',
                        query: {
                            statsPeriod: '90d',
                            project: projectId,
                            per_page: 1,
                        },
                    })];
                case 1:
                    data = _a.sent();
                    return [2 /*return*/, data.length > 0];
            }
        });
    });
}
exports.fetchAnyReleaseExistence = fetchAnyReleaseExistence;
//# sourceMappingURL=projects.jsx.map