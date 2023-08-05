Object.defineProperty(exports, "__esModule", { value: true });
exports.getCurrentMember = exports.resendMemberInvite = exports.updateMember = exports.indexMembersByProject = exports.fetchOrgMembers = void 0;
var tslib_1 = require("tslib");
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var memberActions_1 = tslib_1.__importDefault(require("app/actions/memberActions"));
var memberListStore_1 = tslib_1.__importDefault(require("app/stores/memberListStore"));
function getMemberUser(member) {
    return tslib_1.__assign(tslib_1.__assign({}, member.user), { role: member.role });
}
function fetchOrgMembers(api, orgId, projectIds) {
    if (projectIds === void 0) { projectIds = null; }
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var endpoint, query, members, memberUsers, err_1;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    endpoint = "/organizations/" + orgId + "/users/";
                    query = projectIds ? { project: projectIds } : {};
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, api.requestPromise(endpoint, { method: 'GET', query: query })];
                case 2:
                    members = _a.sent();
                    if (!members) {
                        // This shouldn't happen if the request was successful
                        // It should at least be an empty list
                        Sentry.withScope(function (scope) {
                            scope.setExtras({
                                orgId: orgId,
                                projectIds: projectIds,
                            });
                            Sentry.captureException(new Error('Members is undefined'));
                        });
                    }
                    memberUsers = members === null || members === void 0 ? void 0 : members.filter(function (_a) {
                        var user = _a.user;
                        return user;
                    });
                    if (!memberUsers) {
                        return [2 /*return*/, []];
                    }
                    // Update the store with just the users, as avatars rely on them.
                    memberListStore_1.default.loadInitialData(memberUsers.map(getMemberUser));
                    return [2 /*return*/, members];
                case 3:
                    err_1 = _a.sent();
                    Sentry.setExtras({
                        resp: err_1,
                    });
                    Sentry.captureException(err_1);
                    return [3 /*break*/, 4];
                case 4: return [2 /*return*/, []];
            }
        });
    });
}
exports.fetchOrgMembers = fetchOrgMembers;
/**
 * Convert a list of members with user & project data
 * into a object that maps project slugs : users in that project.
 */
function indexMembersByProject(members) {
    return members.reduce(function (acc, member) {
        var e_1, _a;
        try {
            for (var _b = tslib_1.__values(member.projects), _c = _b.next(); !_c.done; _c = _b.next()) {
                var project = _c.value;
                if (!acc.hasOwnProperty(project)) {
                    acc[project] = [];
                }
                acc[project].push(member.user);
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (_c && !_c.done && (_a = _b.return)) _a.call(_b);
            }
            finally { if (e_1) throw e_1.error; }
        }
        return acc;
    }, {});
}
exports.indexMembersByProject = indexMembersByProject;
function updateMember(api, _a) {
    var orgId = _a.orgId, memberId = _a.memberId, data = _a.data;
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var endpoint, resp, err_2;
        return tslib_1.__generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    memberActions_1.default.update(memberId, data);
                    endpoint = "/organizations/" + orgId + "/members/" + memberId + "/";
                    _b.label = 1;
                case 1:
                    _b.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, api.requestPromise(endpoint, {
                            method: 'PUT',
                            data: data,
                        })];
                case 2:
                    resp = _b.sent();
                    memberActions_1.default.updateSuccess(resp);
                    return [2 /*return*/, resp];
                case 3:
                    err_2 = _b.sent();
                    memberActions_1.default.updateError(err_2);
                    throw err_2;
                case 4: return [2 /*return*/];
            }
        });
    });
}
exports.updateMember = updateMember;
function resendMemberInvite(api, _a) {
    var orgId = _a.orgId, memberId = _a.memberId, regenerate = _a.regenerate, data = _a.data;
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var endpoint, resp, err_3;
        return tslib_1.__generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    memberActions_1.default.resendMemberInvite(orgId, data);
                    endpoint = "/organizations/" + orgId + "/members/" + memberId + "/";
                    _b.label = 1;
                case 1:
                    _b.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, api.requestPromise(endpoint, {
                            method: 'PUT',
                            data: {
                                regenerate: regenerate,
                                reinvite: true,
                            },
                        })];
                case 2:
                    resp = _b.sent();
                    memberActions_1.default.resendMemberInviteSuccess(resp);
                    return [2 /*return*/, resp];
                case 3:
                    err_3 = _b.sent();
                    memberActions_1.default.resendMemberInviteError(err_3);
                    throw err_3;
                case 4: return [2 /*return*/];
            }
        });
    });
}
exports.resendMemberInvite = resendMemberInvite;
function getCurrentMember(api, orgId) {
    return api.requestPromise("/organizations/" + orgId + "/members/me/");
}
exports.getCurrentMember = getCurrentMember;
//# sourceMappingURL=members.jsx.map