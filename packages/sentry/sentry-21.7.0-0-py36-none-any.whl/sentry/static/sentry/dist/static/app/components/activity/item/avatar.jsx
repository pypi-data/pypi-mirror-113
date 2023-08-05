Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var userAvatar_1 = tslib_1.__importDefault(require("app/components/avatar/userAvatar"));
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var icons_1 = require("app/icons");
function ActivityAvatar(_a) {
    var className = _a.className, type = _a.type, user = _a.user, _b = _a.size, size = _b === void 0 ? 38 : _b;
    if (user) {
        return <userAvatar_1.default user={user} size={size} className={className}/>;
    }
    if (type === 'system') {
        // Return Sentry avatar
        return (<SystemAvatar className={className} size={size}>
        <StyledIconSentry size="md"/>
      </SystemAvatar>);
    }
    return (<placeholder_1.default className={className} width={size + "px"} height={size + "px"} shape="circle"/>);
}
exports.default = ActivityAvatar;
var SystemAvatar = styled_1.default('span')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  width: ", "px;\n  height: ", "px;\n  background-color: ", ";\n  color: ", ";\n  border-radius: 50%;\n"], ["\n  display: flex;\n  justify-content: center;\n  align-items: center;\n  width: ", "px;\n  height: ", "px;\n  background-color: ", ";\n  color: ", ";\n  border-radius: 50%;\n"])), function (p) { return p.size; }, function (p) { return p.size; }, function (p) { return p.theme.textColor; }, function (p) { return p.theme.background; });
var StyledIconSentry = styled_1.default(icons_1.IconSentry)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding-bottom: 3px;\n"], ["\n  padding-bottom: 3px;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=avatar.jsx.map