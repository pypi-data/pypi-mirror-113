Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var platformList_1 = tslib_1.__importDefault(require("app/components/platformList"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var ProjectAvatar = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectAvatar, _super);
    function ProjectAvatar() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.getPlatforms = function (project) {
            // `platform` is a user selectable option that is performed during the onboarding process. The reason why this
            // is not the default is because there currently is no way to update it. Fallback to this if project does not
            // have recent events with a platform.
            if (project && project.platform) {
                return [project.platform];
            }
            return [];
        };
        return _this;
    }
    ProjectAvatar.prototype.render = function () {
        var _a = this.props, project = _a.project, hasTooltip = _a.hasTooltip, tooltip = _a.tooltip, props = tslib_1.__rest(_a, ["project", "hasTooltip", "tooltip"]);
        return (<tooltip_1.default disabled={!hasTooltip} title={tooltip}>
        <platformList_1.default platforms={this.getPlatforms(project)} {...props} max={1}/>
      </tooltip_1.default>);
    };
    return ProjectAvatar;
}(react_1.Component));
exports.default = ProjectAvatar;
//# sourceMappingURL=projectAvatar.jsx.map