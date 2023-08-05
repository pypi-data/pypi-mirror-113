Object.defineProperty(exports, "__esModule", { value: true });
exports.fetchOrganizationEnvironments = void 0;
var tslib_1 = require("tslib");
var environmentActions_1 = tslib_1.__importDefault(require("app/actions/environmentActions"));
/**
 * Fetches all environments for an organization
 *
 * @param organizationSlug The organization slug
 */
function fetchOrganizationEnvironments(api, organizationSlug) {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var environments, err_1;
        return tslib_1.__generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    environmentActions_1.default.fetchEnvironments();
                    _a.label = 1;
                case 1:
                    _a.trys.push([1, 3, , 4]);
                    return [4 /*yield*/, api.requestPromise("/organizations/" + organizationSlug + "/environments/")];
                case 2:
                    environments = _a.sent();
                    if (!environments) {
                        environmentActions_1.default.fetchEnvironmentsError(new Error('retrieved environments is falsey'));
                        return [2 /*return*/];
                    }
                    environmentActions_1.default.fetchEnvironmentsSuccess(environments);
                    return [3 /*break*/, 4];
                case 3:
                    err_1 = _a.sent();
                    environmentActions_1.default.fetchEnvironmentsError(err_1);
                    return [3 /*break*/, 4];
                case 4: return [2 /*return*/];
            }
        });
    });
}
exports.fetchOrganizationEnvironments = fetchOrganizationEnvironments;
//# sourceMappingURL=environments.jsx.map