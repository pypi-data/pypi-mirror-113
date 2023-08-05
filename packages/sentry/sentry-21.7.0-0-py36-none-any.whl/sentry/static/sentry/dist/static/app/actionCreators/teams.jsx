Object.defineProperty(exports, "__esModule", { value: true });
exports.removeTeam = exports.createTeam = exports.leaveTeam = exports.joinTeam = exports.updateTeam = exports.updateTeamSuccess = exports.fetchTeamDetails = exports.fetchTeams = void 0;
var tslib_1 = require("tslib");
var indicator_1 = require("app/actionCreators/indicator");
var teamActions_1 = tslib_1.__importDefault(require("app/actions/teamActions"));
var locale_1 = require("app/locale");
var callIfFunction_1 = require("app/utils/callIfFunction");
var guid_1 = require("app/utils/guid");
var doCallback = function (params, name) {
    if (params === void 0) { params = {}; }
    var args = [];
    for (var _i = 2; _i < arguments.length; _i++) {
        args[_i - 2] = arguments[_i];
    }
    callIfFunction_1.callIfFunction.apply(void 0, tslib_1.__spreadArray([params[name]], tslib_1.__read(args)));
};
// Fetch teams for org
function fetchTeams(api, params, options) {
    teamActions_1.default.fetchAll(params.orgId);
    return api.request("/teams/" + params.orgId + "/", {
        success: function (data) {
            teamActions_1.default.fetchAllSuccess(params.orgId, data);
            doCallback(options, 'success', data);
        },
        error: function (error) {
            teamActions_1.default.fetchAllError(params.orgId, error);
            doCallback(options, 'error', error);
        },
    });
}
exports.fetchTeams = fetchTeams;
function fetchTeamDetails(api, params, options) {
    teamActions_1.default.fetchDetails(params.teamId);
    return api.request("/teams/" + params.orgId + "/" + params.teamId + "/", {
        success: function (data) {
            teamActions_1.default.fetchDetailsSuccess(params.teamId, data);
            doCallback(options, 'success', data);
        },
        error: function (error) {
            teamActions_1.default.fetchDetailsError(params.teamId, error);
            doCallback(options, 'error', error);
        },
    });
}
exports.fetchTeamDetails = fetchTeamDetails;
function updateTeamSuccess(teamId, data) {
    teamActions_1.default.updateSuccess(teamId, data);
}
exports.updateTeamSuccess = updateTeamSuccess;
function updateTeam(api, params, options) {
    var endpoint = "/teams/" + params.orgId + "/" + params.teamId + "/";
    teamActions_1.default.update(params.teamId, params.data);
    return api.request(endpoint, {
        method: 'PUT',
        data: params.data,
        success: function (data) {
            updateTeamSuccess(params.teamId, data);
            doCallback(options, 'success', data);
        },
        error: function (error) {
            teamActions_1.default.updateError(params.teamId, error);
            doCallback(options, 'error', error);
        },
    });
}
exports.updateTeam = updateTeam;
function joinTeam(api, params, options) {
    var _a;
    var endpoint = "/organizations/" + params.orgId + "/members/" + ((_a = params.memberId) !== null && _a !== void 0 ? _a : 'me') + "/teams/" + params.teamId + "/";
    var id = guid_1.uniqueId();
    teamActions_1.default.update(id, params.teamId);
    return api.request(endpoint, {
        method: 'POST',
        success: function (data) {
            teamActions_1.default.updateSuccess(params.teamId, data);
            doCallback(options, 'success', data);
        },
        error: function (error) {
            teamActions_1.default.updateError(id, params.teamId, error);
            doCallback(options, 'error', error);
        },
    });
}
exports.joinTeam = joinTeam;
function leaveTeam(api, params, options) {
    var endpoint = "/organizations/" + params.orgId + "/members/" + (params.memberId || 'me') + "/teams/" + params.teamId + "/";
    var id = guid_1.uniqueId();
    teamActions_1.default.update(id, params.teamId);
    return api.request(endpoint, {
        method: 'DELETE',
        success: function (data) {
            teamActions_1.default.updateSuccess(params.teamId, data);
            doCallback(options, 'success', data);
        },
        error: function (error) {
            teamActions_1.default.updateError(id, params.teamId, error);
            doCallback(options, 'error', error);
        },
    });
}
exports.leaveTeam = leaveTeam;
function createTeam(api, team, params) {
    teamActions_1.default.createTeam(team);
    return api
        .requestPromise("/organizations/" + params.orgId + "/teams/", {
        method: 'POST',
        data: team,
    })
        .then(function (data) {
        teamActions_1.default.createTeamSuccess(data);
        indicator_1.addSuccessMessage(locale_1.tct('[team] has been added to the [organization] organization', {
            team: "#" + data.slug,
            organization: params.orgId,
        }));
        return data;
    }, function (err) {
        teamActions_1.default.createTeamError(team.slug, err);
        indicator_1.addErrorMessage(locale_1.tct('Unable to create [team] in the [organization] organization', {
            team: "#" + team.slug,
            organization: params.orgId,
        }));
        throw err;
    });
}
exports.createTeam = createTeam;
function removeTeam(api, params) {
    teamActions_1.default.removeTeam(params.teamId);
    return api
        .requestPromise("/teams/" + params.orgId + "/" + params.teamId + "/", {
        method: 'DELETE',
    })
        .then(function (data) {
        teamActions_1.default.removeTeamSuccess(params.teamId, data);
        indicator_1.addSuccessMessage(locale_1.tct('[team] has been removed from the [organization] organization', {
            team: "#" + params.teamId,
            organization: params.orgId,
        }));
        return data;
    }, function (err) {
        teamActions_1.default.removeTeamError(params.teamId, err);
        indicator_1.addErrorMessage(locale_1.tct('Unable to remove [team] from the [organization] organization', {
            team: "#" + params.teamId,
            organization: params.orgId,
        }));
        throw err;
    });
}
exports.removeTeam = removeTeam;
//# sourceMappingURL=teams.jsx.map