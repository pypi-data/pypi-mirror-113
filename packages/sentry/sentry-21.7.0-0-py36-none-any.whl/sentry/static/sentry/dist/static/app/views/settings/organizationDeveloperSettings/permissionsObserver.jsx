Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var consolidatedScopes_1 = require("app/utils/consolidatedScopes");
var permissionSelection_1 = tslib_1.__importDefault(require("app/views/settings/organizationDeveloperSettings/permissionSelection"));
var resourceSubscriptions_1 = tslib_1.__importDefault(require("app/views/settings/organizationDeveloperSettings/resourceSubscriptions"));
var PermissionsObserver = /** @class */ (function (_super) {
    tslib_1.__extends(PermissionsObserver, _super);
    function PermissionsObserver(props) {
        var _this = _super.call(this, props) || this;
        _this.onPermissionChange = function (permissions) {
            _this.setState({ permissions: permissions });
        };
        _this.onEventChange = function (events) {
            _this.setState({ events: events });
        };
        _this.state = {
            permissions: _this.scopeListToPermissionState(),
            events: _this.props.events,
        };
        return _this;
    }
    /**
     * Converts the list of raw API scopes passed in to an object that can
     * before stored and used via `state`. This object is structured by
     * resource and holds "Permission" values. For example:
     *
     *    {
     *      'Project': 'read',
     *      ...,
     *    }
     *
     */
    PermissionsObserver.prototype.scopeListToPermissionState = function () {
        return consolidatedScopes_1.toResourcePermissions(this.props.scopes);
    };
    PermissionsObserver.prototype.render = function () {
        var _a = this.state, permissions = _a.permissions, events = _a.events;
        return (<react_1.Fragment>
        <panels_1.Panel>
          <panels_1.PanelHeader>{locale_1.t('Permissions')}</panels_1.PanelHeader>
          <panels_1.PanelBody>
            <permissionSelection_1.default permissions={permissions} onChange={this.onPermissionChange} appPublished={this.props.appPublished}/>
          </panels_1.PanelBody>
        </panels_1.Panel>
        <panels_1.Panel>
          <panels_1.PanelHeader>{locale_1.t('Webhooks')}</panels_1.PanelHeader>
          <panels_1.PanelBody>
            <resourceSubscriptions_1.default permissions={permissions} events={events} onChange={this.onEventChange} webhookDisabled={this.props.webhookDisabled}/>
          </panels_1.PanelBody>
        </panels_1.Panel>
      </react_1.Fragment>);
    };
    PermissionsObserver.defaultProps = {
        webhookDisabled: false,
        appPublished: false,
    };
    return PermissionsObserver;
}(react_1.Component));
exports.default = PermissionsObserver;
//# sourceMappingURL=permissionsObserver.jsx.map