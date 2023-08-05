Object.defineProperty(exports, "__esModule", { value: true });
exports.mergeGroups = exports.bulkUpdate = exports.bulkDelete = exports.paramsToQueryArgs = exports.updateNote = exports.createNote = exports.deleteNote = exports.assignToActor = exports.clearAssignment = exports.assignToUser = void 0;
var tslib_1 = require("tslib");
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var isNil_1 = tslib_1.__importDefault(require("lodash/isNil"));
var groupActions_1 = tslib_1.__importDefault(require("app/actions/groupActions"));
var api_1 = require("app/api");
var groupStore_1 = tslib_1.__importDefault(require("app/stores/groupStore"));
var utils_1 = require("app/utils");
var guid_1 = require("app/utils/guid");
function assignToUser(params) {
    var api = new api_1.Client();
    var endpoint = "/issues/" + params.id + "/";
    var id = guid_1.uniqueId();
    groupActions_1.default.assignTo(id, params.id, {
        email: (params.member && params.member.email) || '',
    });
    var request = api.requestPromise(endpoint, {
        method: 'PUT',
        // Sending an empty value to assignedTo is the same as "clear",
        // so if no member exists, that implies that we want to clear the
        // current assignee.
        data: {
            assignedTo: params.user ? utils_1.buildUserId(params.user.id) : '',
        },
    });
    request
        .then(function (data) {
        groupActions_1.default.assignToSuccess(id, params.id, data);
    })
        .catch(function (data) {
        groupActions_1.default.assignToError(id, params.id, data);
    });
    return request;
}
exports.assignToUser = assignToUser;
function clearAssignment(groupId) {
    var api = new api_1.Client();
    var endpoint = "/issues/" + groupId + "/";
    var id = guid_1.uniqueId();
    groupActions_1.default.assignTo(id, groupId, {
        email: '',
    });
    var request = api.requestPromise(endpoint, {
        method: 'PUT',
        // Sending an empty value to assignedTo is the same as "clear"
        data: {
            assignedTo: '',
        },
    });
    request
        .then(function (data) {
        groupActions_1.default.assignToSuccess(id, groupId, data);
    })
        .catch(function (data) {
        groupActions_1.default.assignToError(id, groupId, data);
    });
    return request;
}
exports.clearAssignment = clearAssignment;
function assignToActor(_a) {
    var id = _a.id, actor = _a.actor;
    var api = new api_1.Client();
    var endpoint = "/issues/" + id + "/";
    var guid = guid_1.uniqueId();
    var actorId;
    groupActions_1.default.assignTo(guid, id, { email: '' });
    switch (actor.type) {
        case 'user':
            actorId = utils_1.buildUserId(actor.id);
            break;
        case 'team':
            actorId = utils_1.buildTeamId(actor.id);
            break;
        default:
            Sentry.withScope(function (scope) {
                scope.setExtra('actor', actor);
                Sentry.captureException('Unknown assignee type');
            });
    }
    return api
        .requestPromise(endpoint, {
        method: 'PUT',
        data: { assignedTo: actorId },
    })
        .then(function (data) {
        groupActions_1.default.assignToSuccess(guid, id, data);
    })
        .catch(function (data) {
        groupActions_1.default.assignToError(guid, id, data);
    });
}
exports.assignToActor = assignToActor;
function deleteNote(api, group, id, _oldText) {
    var restore = group.activity.find(function (activity) { return activity.id === id; });
    var index = groupStore_1.default.removeActivity(group.id, id);
    if (index === -1) {
        // I dunno, the id wasn't found in the GroupStore
        return Promise.reject(new Error('Group was not found in store'));
    }
    var promise = api.requestPromise("/issues/" + group.id + "/comments/" + id + "/", {
        method: 'DELETE',
    });
    promise.catch(function () { return groupStore_1.default.addActivity(group.id, restore, index); });
    return promise;
}
exports.deleteNote = deleteNote;
function createNote(api, group, note) {
    var promise = api.requestPromise("/issues/" + group.id + "/comments/", {
        method: 'POST',
        data: note,
    });
    promise.then(function (data) { return groupStore_1.default.addActivity(group.id, data); });
    return promise;
}
exports.createNote = createNote;
function updateNote(api, group, note, id, oldText) {
    groupStore_1.default.updateActivity(group.id, id, { text: note.text });
    var promise = api.requestPromise("/issues/" + group.id + "/comments/" + id + "/", {
        method: 'PUT',
        data: note,
    });
    promise.catch(function () { return groupStore_1.default.updateActivity(group.id, id, { text: oldText }); });
    return promise;
}
exports.updateNote = updateNote;
/**
 * Converts input parameters to API-compatible query arguments
 */
function paramsToQueryArgs(params) {
    var _a;
    var p = params.itemIds
        ? { id: params.itemIds } // items matching array of itemids
        : params.query
            ? { query: params.query } // items matching search query
            : {}; // all items
    // only include environment if it is not null/undefined
    if (params.query && !isNil_1.default(params.environment)) {
        p.environment = params.environment;
    }
    // only include projects if it is not null/undefined/an empty array
    if ((_a = params.project) === null || _a === void 0 ? void 0 : _a.length) {
        p.project = params.project;
    }
    // only include date filters if they are not null/undefined
    if (params.query) {
        ['start', 'end', 'period', 'utc'].forEach(function (prop) {
            if (!isNil_1.default(params[prop])) {
                p[prop === 'period' ? 'statsPeriod' : prop] = params[prop];
            }
        });
    }
    return p;
}
exports.paramsToQueryArgs = paramsToQueryArgs;
function getUpdateUrl(_a) {
    var projectId = _a.projectId, orgId = _a.orgId;
    return projectId
        ? "/projects/" + orgId + "/" + projectId + "/issues/"
        : "/organizations/" + orgId + "/issues/";
}
function chainUtil() {
    var funcs = [];
    for (var _i = 0; _i < arguments.length; _i++) {
        funcs[_i] = arguments[_i];
    }
    var filteredFuncs = funcs.filter(function (f) { return typeof f === 'function'; });
    return function () {
        var args = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            args[_i] = arguments[_i];
        }
        filteredFuncs.forEach(function (func) {
            func.apply(funcs, args);
        });
    };
}
function wrapRequest(api, path, options, extraParams) {
    if (extraParams === void 0) { extraParams = {}; }
    options.success = chainUtil(options.success, extraParams.success);
    options.error = chainUtil(options.error, extraParams.error);
    options.complete = chainUtil(options.complete, extraParams.complete);
    return api.request(path, options);
}
function bulkDelete(api, params, options) {
    var itemIds = params.itemIds;
    var path = getUpdateUrl(params);
    var query = paramsToQueryArgs(params);
    var id = guid_1.uniqueId();
    groupActions_1.default.delete(id, itemIds);
    return wrapRequest(api, path, {
        query: query,
        method: 'DELETE',
        success: function (response) {
            groupActions_1.default.deleteSuccess(id, itemIds, response);
        },
        error: function (error) {
            groupActions_1.default.deleteError(id, itemIds, error);
        },
    }, options);
}
exports.bulkDelete = bulkDelete;
function bulkUpdate(api, params, options) {
    var itemIds = params.itemIds, failSilently = params.failSilently, data = params.data;
    var path = getUpdateUrl(params);
    var query = paramsToQueryArgs(params);
    var id = guid_1.uniqueId();
    groupActions_1.default.update(id, itemIds, data);
    return wrapRequest(api, path, {
        query: query,
        method: 'PUT',
        data: data,
        success: function (response) {
            groupActions_1.default.updateSuccess(id, itemIds, response);
        },
        error: function (error) {
            groupActions_1.default.updateError(id, itemIds, error, failSilently);
        },
    }, options);
}
exports.bulkUpdate = bulkUpdate;
function mergeGroups(api, params, options) {
    var itemIds = params.itemIds;
    var path = getUpdateUrl(params);
    var query = paramsToQueryArgs(params);
    var id = guid_1.uniqueId();
    groupActions_1.default.merge(id, itemIds);
    return wrapRequest(api, path, {
        query: query,
        method: 'PUT',
        data: { merge: 1 },
        success: function (response) {
            groupActions_1.default.mergeSuccess(id, itemIds, response);
        },
        error: function (error) {
            groupActions_1.default.mergeError(id, itemIds, error);
        },
    }, options);
}
exports.mergeGroups = mergeGroups;
//# sourceMappingURL=group.jsx.map