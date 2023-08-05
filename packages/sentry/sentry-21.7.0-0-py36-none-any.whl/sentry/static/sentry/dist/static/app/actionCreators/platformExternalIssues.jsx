Object.defineProperty(exports, "__esModule", { value: true });
exports.deleteExternalIssue = void 0;
var tslib_1 = require("tslib");
var platformExternalIssueActions_1 = tslib_1.__importDefault(require("app/actions/platformExternalIssueActions"));
function deleteExternalIssue(api, groupId, externalIssueId) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var data, error_1;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    platformExternalIssueActions_1.default.delete(groupId, externalIssueId);
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, api.requestPromise("/issues/" + groupId + "/external-issues/" + externalIssueId + "/", {
                            method: 'DELETE',
                        })];
                case 2:
                    data = _a.sent();
                    platformExternalIssueActions_1.default.deleteSuccess(data);
                    return [2 /*return*/, data];
                case 3:
                    error_1 = _a.sent();
                    platformExternalIssueActions_1.default.deleteError(error_1);
                    throw error_1;
                case 4: return [2 /*return*/];
            }
        });
    });
}
exports.deleteExternalIssue = deleteExternalIssue;
//# sourceMappingURL=platformExternalIssues.jsx.map