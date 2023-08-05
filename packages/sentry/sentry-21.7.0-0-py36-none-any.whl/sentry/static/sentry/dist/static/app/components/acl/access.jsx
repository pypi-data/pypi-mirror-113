Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var isRenderFunc_1 = require("app/utils/isRenderFunc");
var withConfig_1 = tslib_1.__importDefault(require("app/utils/withConfig"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var DEFAULT_NO_ACCESS_MESSAGE = (<alert_1.default type="error" icon={<icons_1.IconInfo size="md"/>}>
    {locale_1.t('You do not have sufficient permissions to access this.')}
  </alert_1.default>);
var defaultProps = {
    renderNoAccessMessage: false,
    isSuperuser: false,
    requireAll: true,
    access: [],
};
/**
 * Component to handle access restrictions.
 */
var Access = /** @class */ (function (_super) {
    tslib_1.__extends(Access, _super);
    function Access() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Access.prototype.render = function () {
        var _a = this.props, organization = _a.organization, config = _a.config, access = _a.access, requireAll = _a.requireAll, isSuperuser = _a.isSuperuser, renderNoAccessMessage = _a.renderNoAccessMessage, children = _a.children;
        var orgAccess = (organization || { access: [] }).access;
        var method = requireAll ? 'every' : 'some';
        var hasAccess = !access || access[method](function (acc) { return orgAccess.includes(acc); });
        var hasSuperuser = !!(config.user && config.user.isSuperuser);
        var renderProps = {
            hasAccess: hasAccess,
            hasSuperuser: hasSuperuser,
        };
        var render = hasAccess && (!isSuperuser || hasSuperuser);
        if (!render && typeof renderNoAccessMessage === 'function') {
            return renderNoAccessMessage(renderProps);
        }
        else if (!render && renderNoAccessMessage) {
            return DEFAULT_NO_ACCESS_MESSAGE;
        }
        if (isRenderFunc_1.isRenderFunc(children)) {
            return children(renderProps);
        }
        return render ? children : null;
    };
    Access.defaultProps = defaultProps;
    return Access;
}(React.Component));
exports.default = withOrganization_1.default(withConfig_1.default(Access));
//# sourceMappingURL=access.jsx.map