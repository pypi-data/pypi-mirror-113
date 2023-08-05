Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var PermissionAlert = function (_a) {
    var _b = _a.access, access = _b === void 0 ? ['project:write'] : _b, props = tslib_1.__rest(_a, ["access"]);
    return (<access_1.default access={access}>
    {function (_a) {
            var hasAccess = _a.hasAccess;
            return !hasAccess && (<alert_1.default type="warning" icon={<icons_1.IconWarning size="xs"/>} {...props}>
          {locale_1.t('These settings can only be edited by users with the organization owner, manager, or admin role.')}
        </alert_1.default>);
        }}
  </access_1.default>);
};
exports.default = PermissionAlert;
//# sourceMappingURL=permissionAlert.jsx.map