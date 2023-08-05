Object.defineProperty(exports, "__esModule", { value: true });
exports.markIncidentAsSeen = exports.updateIncidentNote = exports.deleteIncidentNote = exports.createIncidentNote = exports.fetchIncidentActivities = void 0;
var tslib_1 = require("tslib");
var indicator_1 = require("app/actionCreators/indicator");
var locale_1 = require("app/locale");
/**
 * Fetches a list of activities for an incident
 */
function fetchIncidentActivities(api, orgId, alertId) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        return tslib_1.__generator(this, function (_a) {
            return [2 /*return*/, api.requestPromise("/organizations/" + orgId + "/incidents/" + alertId + "/activity/")];
        });
    });
}
exports.fetchIncidentActivities = fetchIncidentActivities;
/**
 * Creates a note for an incident
 */
function createIncidentNote(api, orgId, alertId, note) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var result, err_1;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 2, , 3]);
                    return [4 /*yield*/, api.requestPromise("/organizations/" + orgId + "/incidents/" + alertId + "/comments/", {
                            method: 'POST',
                            data: {
                                mentions: note.mentions,
                                comment: note.text,
                            },
                        })];
                case 1:
                    result = _a.sent();
                    return [2 /*return*/, result];
                case 2:
                    err_1 = _a.sent();
                    indicator_1.addErrorMessage(locale_1.t('Unable to post comment'));
                    throw err_1;
                case 3: return [2 /*return*/];
            }
        });
    });
}
exports.createIncidentNote = createIncidentNote;
/**
 * Deletes a note for an incident
 */
function deleteIncidentNote(api, orgId, alertId, noteId) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var result, err_2;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 2, , 3]);
                    return [4 /*yield*/, api.requestPromise("/organizations/" + orgId + "/incidents/" + alertId + "/comments/" + noteId + "/", {
                            method: 'DELETE',
                        })];
                case 1:
                    result = _a.sent();
                    return [2 /*return*/, result];
                case 2:
                    err_2 = _a.sent();
                    indicator_1.addErrorMessage(locale_1.t('Failed to delete comment'));
                    throw err_2;
                case 3: return [2 /*return*/];
            }
        });
    });
}
exports.deleteIncidentNote = deleteIncidentNote;
/**
 * Updates a note for an incident
 */
function updateIncidentNote(api, orgId, alertId, noteId, note) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var result, err_3;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 2, , 3]);
                    return [4 /*yield*/, api.requestPromise("/organizations/" + orgId + "/incidents/" + alertId + "/comments/" + noteId + "/", {
                            method: 'PUT',
                            data: {
                                mentions: note.mentions,
                                comment: note.text,
                            },
                        })];
                case 1:
                    result = _a.sent();
                    indicator_1.clearIndicators();
                    return [2 /*return*/, result];
                case 2:
                    err_3 = _a.sent();
                    indicator_1.addErrorMessage(locale_1.t('Unable to update comment'));
                    throw err_3;
                case 3: return [2 /*return*/];
            }
        });
    });
}
exports.updateIncidentNote = updateIncidentNote;
// This doesn't return anything because you shouldn't need to do anything with
// the result success or fail
function markIncidentAsSeen(api, orgId, incident) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var err_4;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    if (!incident || incident.hasSeen) {
                        return [2 /*return*/];
                    }
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, api.requestPromise("/organizations/" + orgId + "/incidents/" + incident.identifier + "/seen/", {
                            method: 'POST',
                            data: {
                                hasSeen: true,
                            },
                        })];
                case 2:
                    _a.sent();
                    return [3 /*break*/, 4];
                case 3:
                    err_4 = _a.sent();
                    return [3 /*break*/, 4];
                case 4: return [2 /*return*/];
            }
        });
    });
}
exports.markIncidentAsSeen = markIncidentAsSeen;
//# sourceMappingURL=incident.jsx.map