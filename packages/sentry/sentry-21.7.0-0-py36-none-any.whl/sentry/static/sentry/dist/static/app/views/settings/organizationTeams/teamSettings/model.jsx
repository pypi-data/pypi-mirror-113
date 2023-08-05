Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var teams_1 = require("app/actionCreators/teams");
var model_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/model"));
var TeamFormModel = /** @class */ (function (_super) {
    tslib_1.__extends(TeamFormModel, _super);
    function TeamFormModel(orgId, teamId) {
        var _this = _super.call(this) || this;
        _this.orgId = orgId;
        _this.teamId = teamId;
        return _this;
    }
    TeamFormModel.prototype.doApiRequest = function (_a) {
        var _this = this;
        var data = _a.data;
        return new Promise(function (resolve, reject) {
            return teams_1.updateTeam(_this.api, {
                orgId: _this.orgId,
                teamId: _this.teamId,
                data: data,
            }, {
                success: resolve,
                error: reject,
            });
        });
    };
    return TeamFormModel;
}(model_1.default));
exports.default = TeamFormModel;
//# sourceMappingURL=model.jsx.map