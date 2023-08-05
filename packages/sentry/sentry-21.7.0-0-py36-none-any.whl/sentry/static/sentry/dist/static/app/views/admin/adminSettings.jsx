Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var isUndefined_1 = tslib_1.__importDefault(require("lodash/isUndefined"));
var forms_1 = require("app/components/forms");
var locale_1 = require("app/locale");
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var options_1 = require("./options");
var optionsAvailable = [
    'system.url-prefix',
    'system.admin-email',
    'system.support-email',
    'system.security-email',
    'system.rate-limit',
    'auth.allow-registration',
    'auth.ip-rate-limit',
    'auth.user-rate-limit',
    'api.rate-limit.org-create',
    'beacon.anonymous',
];
var AdminSettings = /** @class */ (function (_super) {
    tslib_1.__extends(AdminSettings, _super);
    function AdminSettings() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Object.defineProperty(AdminSettings.prototype, "endpoint", {
        get: function () {
            return '/internal/options/';
        },
        enumerable: false,
        configurable: true
    });
    AdminSettings.prototype.getEndpoints = function () {
        return [['data', this.endpoint]];
    };
    AdminSettings.prototype.renderBody = function () {
        var e_1, _a;
        var _b;
        var data = this.state.data;
        var initialData = {};
        var fields = {};
        try {
            for (var optionsAvailable_1 = tslib_1.__values(optionsAvailable), optionsAvailable_1_1 = optionsAvailable_1.next(); !optionsAvailable_1_1.done; optionsAvailable_1_1 = optionsAvailable_1.next()) {
                var key = optionsAvailable_1_1.value;
                // TODO(dcramer): we should not be mutating options
                var option = (_b = data[key]) !== null && _b !== void 0 ? _b : { field: {}, value: undefined };
                if (isUndefined_1.default(option.value) || option.value === '') {
                    var defn = options_1.getOption(key);
                    initialData[key] = defn.defaultValue ? defn.defaultValue() : '';
                }
                else {
                    initialData[key] = option.value;
                }
                fields[key] = options_1.getOptionField(key, option.field);
            }
        }
        catch (e_1_1) { e_1 = { error: e_1_1 }; }
        finally {
            try {
                if (optionsAvailable_1_1 && !optionsAvailable_1_1.done && (_a = optionsAvailable_1.return)) _a.call(optionsAvailable_1);
            }
            finally { if (e_1) throw e_1.error; }
        }
        return (<div>
        <h3>{locale_1.t('Settings')}</h3>

        <forms_1.ApiForm apiMethod="PUT" apiEndpoint={this.endpoint} initialData={initialData} omitDisabled requireChanges>
          <h4>General</h4>
          {fields['system.url-prefix']}
          {fields['system.admin-email']}
          {fields['system.support-email']}
          {fields['system.security-email']}
          {fields['system.rate-limit']}

          <h4>Security & Abuse</h4>
          {fields['auth.allow-registration']}
          {fields['auth.ip-rate-limit']}
          {fields['auth.user-rate-limit']}
          {fields['api.rate-limit.org-create']}

          <h4>Beacon</h4>
          {fields['beacon.anonymous']}
        </forms_1.ApiForm>
      </div>);
    };
    return AdminSettings;
}(asyncView_1.default));
exports.default = AdminSettings;
//# sourceMappingURL=adminSettings.jsx.map