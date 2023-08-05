Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var baseAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/baseAvatar"));
var utils_1 = require("app/utils");
var TeamAvatar = /** @class */ (function (_super) {
    tslib_1.__extends(TeamAvatar, _super);
    function TeamAvatar() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    TeamAvatar.prototype.render = function () {
        var _a = this.props, team = _a.team, tooltipProp = _a.tooltip, props = tslib_1.__rest(_a, ["team", "tooltip"]);
        if (!team) {
            return null;
        }
        var slug = (team && team.slug) || '';
        var title = utils_1.explodeSlug(slug);
        var tooltip = tooltipProp !== null && tooltipProp !== void 0 ? tooltipProp : "#" + title;
        return (<baseAvatar_1.default {...props} type={(team.avatar && team.avatar.avatarType) || 'letter_avatar'} uploadPath="team-avatar" uploadId={team.avatar && team.avatar.avatarUuid} letterId={slug} tooltip={tooltip} title={title}/>);
    };
    return TeamAvatar;
}(react_1.Component));
exports.default = TeamAvatar;
//# sourceMappingURL=teamAvatar.jsx.map