Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var userAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/userAvatar"));
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var UserBadge = function (_a) {
    var _b = _a.avatarSize, avatarSize = _b === void 0 ? 24 : _b, _c = _a.hideEmail, hideEmail = _c === void 0 ? false : _c, displayName = _a.displayName, displayEmail = _a.displayEmail, user = _a.user, className = _a.className;
    var title = displayName ||
        (user &&
            (user.name ||
                user.email ||
                user.username ||
                user.ipAddress ||
                // Because this can be used to render EventUser models, or User *interface*
                // objects from serialized Event models. we try both ipAddress and ip_address.
                user.ip_address ||
                user.id));
    return (<StyledUserBadge className={className}>
      <StyledAvatar user={user} size={avatarSize}/>
      <StyledNameAndEmail>
        <StyledName hideEmail={!!hideEmail}>{title}</StyledName>
        {!hideEmail && <StyledEmail>{displayEmail || (user && user.email)}</StyledEmail>}
      </StyledNameAndEmail>
    </StyledUserBadge>);
};
var StyledUserBadge = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var StyledNameAndEmail = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  flex-shrink: 1;\n  min-width: 0;\n  line-height: 1;\n"], ["\n  flex-shrink: 1;\n  min-width: 0;\n  line-height: 1;\n"])));
var StyledEmail = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-size: 0.875em;\n  margin-top: ", ";\n  color: ", ";\n  ", ";\n"], ["\n  font-size: 0.875em;\n  margin-top: ", ";\n  color: ", ";\n  ", ";\n"])), space_1.default(0.25), function (p) { return p.theme.gray300; }, overflowEllipsis_1.default);
var StyledName = styled_1.default('span')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  font-weight: ", ";\n  line-height: 1.15em;\n  ", ";\n"], ["\n  font-weight: ", ";\n  line-height: 1.15em;\n  ", ";\n"])), function (p) { return (p.hideEmail ? 'inherit' : 'bold'); }, overflowEllipsis_1.default);
var StyledAvatar = styled_1.default(userAvatar_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  min-width: ", ";\n  min-height: ", ";\n  margin-right: ", ";\n"], ["\n  min-width: ", ";\n  min-height: ", ";\n  margin-right: ", ";\n"])), space_1.default(3), space_1.default(3), space_1.default(1));
exports.default = UserBadge;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=userBadge.jsx.map