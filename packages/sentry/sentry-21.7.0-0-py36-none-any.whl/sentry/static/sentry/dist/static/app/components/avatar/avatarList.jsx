Object.defineProperty(exports, "__esModule", { value: true });
exports.AvatarListWrapper = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_2 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var userAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/userAvatar"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var defaultProps = {
    avatarSize: 28,
    maxVisibleAvatars: 5,
    typeMembers: 'users',
    tooltipOptions: {},
};
var AvatarList = /** @class */ (function (_super) {
    tslib_1.__extends(AvatarList, _super);
    function AvatarList() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AvatarList.prototype.render = function () {
        var _a = this.props, className = _a.className, users = _a.users, avatarSize = _a.avatarSize, maxVisibleAvatars = _a.maxVisibleAvatars, renderTooltip = _a.renderTooltip, typeMembers = _a.typeMembers, tooltipOptions = _a.tooltipOptions;
        var visibleUsers = users.slice(0, maxVisibleAvatars);
        var numCollapsedUsers = users.length - visibleUsers.length;
        if (!tooltipOptions.position) {
            tooltipOptions.position = 'top';
        }
        return (<exports.AvatarListWrapper className={className}>
        {!!numCollapsedUsers && (<tooltip_1.default title={numCollapsedUsers + " other " + typeMembers}>
            <CollapsedUsers size={avatarSize} data-test-id="avatarList-collapsedusers">
              {numCollapsedUsers < 99 && <Plus>+</Plus>}
              {numCollapsedUsers}
            </CollapsedUsers>
          </tooltip_1.default>)}
        {visibleUsers.map(function (user) { return (<StyledAvatar key={user.id + "-" + user.email} user={user} size={avatarSize} renderTooltip={renderTooltip} tooltipOptions={tooltipOptions} hasTooltip/>); })}
      </exports.AvatarListWrapper>);
    };
    AvatarList.defaultProps = defaultProps;
    return AvatarList;
}(react_1.Component));
exports.default = AvatarList;
// used in releases list page to do some alignment
exports.AvatarListWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: row-reverse;\n"], ["\n  display: flex;\n  flex-direction: row-reverse;\n"])));
var Circle = function (p) { return react_2.css(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  border-radius: 50%;\n  border: 2px solid ", ";\n  margin-left: -8px;\n  cursor: default;\n\n  &:hover {\n    z-index: 1;\n  }\n"], ["\n  border-radius: 50%;\n  border: 2px solid ", ";\n  margin-left: -8px;\n  cursor: default;\n\n  &:hover {\n    z-index: 1;\n  }\n"])), p.theme.background); };
var StyledAvatar = styled_1.default(userAvatar_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  overflow: hidden;\n  ", ";\n"], ["\n  overflow: hidden;\n  ", ";\n"])), Circle);
var CollapsedUsers = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  position: relative;\n  text-align: center;\n  font-weight: 600;\n  background-color: ", ";\n  color: ", ";\n  font-size: ", "px;\n  width: ", "px;\n  height: ", "px;\n  ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  position: relative;\n  text-align: center;\n  font-weight: 600;\n  background-color: ", ";\n  color: ", ";\n  font-size: ", "px;\n  width: ", "px;\n  height: ", "px;\n  ", ";\n"])), function (p) { return p.theme.gray200; }, function (p) { return p.theme.gray300; }, function (p) { return Math.floor(p.size / 2.3); }, function (p) { return p.size; }, function (p) { return p.size; }, Circle);
var Plus = styled_1.default('span')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  font-size: 10px;\n  margin-left: 1px;\n  margin-right: -1px;\n"], ["\n  font-size: 10px;\n  margin-left: 1px;\n  margin-right: -1px;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=avatarList.jsx.map