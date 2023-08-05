Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var find_1 = tslib_1.__importDefault(require("lodash/find"));
var flatMap_1 = tslib_1.__importDefault(require("lodash/flatMap"));
var constants_1 = require("app/constants");
var locale_1 = require("app/locale");
var formContext_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/formContext"));
var selectField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/selectField"));
var PermissionSelection = /** @class */ (function (_super) {
    tslib_1.__extends(PermissionSelection, _super);
    function PermissionSelection() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            permissions: _this.props.permissions,
        };
        _this.onChange = function (resource, choice) {
            var permissions = _this.state.permissions;
            permissions[resource] = choice;
            _this.save(permissions);
        };
        _this.save = function (permissions) {
            _this.setState({ permissions: permissions });
            _this.props.onChange(permissions);
            _this.context.form.setValue('scopes', _this.permissionStateToList());
        };
        return _this;
    }
    /**
     * Converts the "Permission" values held in `state` to a list of raw
     * API scopes we can send to the server. For example:
     *
     *    ['org:read', 'org:write', ...]
     *
     */
    PermissionSelection.prototype.permissionStateToList = function () {
        var permissions = this.state.permissions;
        var findResource = function (r) { return find_1.default(constants_1.SENTRY_APP_PERMISSIONS, ['resource', r]); };
        return flatMap_1.default(Object.entries(permissions), function (_a) {
            var _b, _c, _d;
            var _e = tslib_1.__read(_a, 2), r = _e[0], p = _e[1];
            return (_d = (_c = (_b = findResource(r)) === null || _b === void 0 ? void 0 : _b.choices) === null || _c === void 0 ? void 0 : _c[p]) === null || _d === void 0 ? void 0 : _d.scopes;
        });
    };
    PermissionSelection.prototype.render = function () {
        var _this = this;
        var permissions = this.state.permissions;
        return (<react_1.Fragment>
        {constants_1.SENTRY_APP_PERMISSIONS.map(function (config) {
                var toChoice = function (_a) {
                    var _b = tslib_1.__read(_a, 2), value = _b[0], opt = _b[1];
                    return [value, opt.label];
                };
                var choices = Object.entries(config.choices).map(toChoice);
                var value = permissions[config.resource];
                return (<selectField_1.default 
                // These are not real fields we want submitted, so we use
                // `--permission` as a suffix here, then filter these
                // fields out when submitting the form in
                // sentryApplicationDetails.jsx
                name={config.resource + "--permission"} key={config.resource} choices={choices} help={locale_1.t(config.help)} label={locale_1.t(config.label || config.resource)} onChange={_this.onChange.bind(_this, config.resource)} value={value} defaultValue={value} disabled={_this.props.appPublished} disabledReason={locale_1.t('Cannot update permissions on a published integration')}/>);
            })}
      </react_1.Fragment>);
    };
    PermissionSelection.contextType = formContext_1.default;
    return PermissionSelection;
}(react_1.Component));
exports.default = PermissionSelection;
//# sourceMappingURL=permissionSelection.jsx.map