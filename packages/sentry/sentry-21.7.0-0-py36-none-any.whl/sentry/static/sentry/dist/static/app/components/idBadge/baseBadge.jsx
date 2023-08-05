Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var avatar_1 = tslib_1.__importDefault(require("app/components/avatar"));
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var BaseBadge = React.memo(function (_a) {
    var displayName = _a.displayName, _b = _a.hideName, hideName = _b === void 0 ? false : _b, _c = _a.hideAvatar, hideAvatar = _c === void 0 ? false : _c, _d = _a.avatarProps, avatarProps = _d === void 0 ? {} : _d, _e = _a.avatarSize, avatarSize = _e === void 0 ? 24 : _e, description = _a.description, team = _a.team, organization = _a.organization, project = _a.project, className = _a.className;
    return (<Wrapper className={className}>
      {!hideAvatar && (<StyledAvatar {...avatarProps} size={avatarSize} hideName={hideName} team={team} organization={organization} project={project}/>)}

      {(!hideName || !!description) && (<DisplayNameAndDescription>
          {!hideName && (<DisplayName data-test-id="badge-display-name">{displayName}</DisplayName>)}
          {!!description && <Description>{description}</Description>}
        </DisplayNameAndDescription>)}
    </Wrapper>);
});
exports.default = BaseBadge;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  flex-shrink: 0;\n"], ["\n  display: flex;\n  align-items: center;\n  flex-shrink: 0;\n"])));
var StyledAvatar = styled_1.default(avatar_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n  flex-shrink: 0;\n"], ["\n  margin-right: ", ";\n  flex-shrink: 0;\n"])), function (p) { return (p.hideName ? 0 : space_1.default(1)); });
var DisplayNameAndDescription = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  line-height: 1;\n  overflow: hidden;\n"], ["\n  display: flex;\n  flex-direction: column;\n  line-height: 1;\n  overflow: hidden;\n"])));
var DisplayName = styled_1.default('span')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  overflow: hidden;\n  text-overflow: ellipsis;\n  line-height: 1.2;\n"], ["\n  overflow: hidden;\n  text-overflow: ellipsis;\n  line-height: 1.2;\n"])));
var Description = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  font-size: 0.875em;\n  margin-top: ", ";\n  color: ", ";\n  line-height: 14px;\n  ", ";\n"], ["\n  font-size: 0.875em;\n  margin-top: ", ";\n  color: ", ";\n  line-height: 14px;\n  ", ";\n"])), space_1.default(0.25), function (p) { return p.theme.gray300; }, overflowEllipsis_1.default);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=baseBadge.jsx.map