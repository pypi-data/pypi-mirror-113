Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var locale_1 = require("app/locale");
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var AdminPackages = /** @class */ (function (_super) {
    tslib_1.__extends(AdminPackages, _super);
    function AdminPackages() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AdminPackages.prototype.getEndpoints = function () {
        return [['data', '/internal/packages/']];
    };
    AdminPackages.prototype.renderBody = function () {
        var data = this.state.data;
        var extensions = data.extensions, modules = data.modules;
        return (<div>
        <h3>{locale_1.t('Extensions')}</h3>

        {extensions.length > 0 ? (<dl className="vars">
            {extensions.map(function (_a) {
                    var _b = tslib_1.__read(_a, 2), key = _b[0], value = _b[1];
                    return (<react_1.Fragment key={key}>
                <dt>{key}</dt>
                <dd>
                  <pre className="val">{value}</pre>
                </dd>
              </react_1.Fragment>);
                })}
          </dl>) : (<p>{locale_1.t('No extensions registered')}</p>)}

        <h3>{locale_1.t('Modules')}</h3>

        {modules.length > 0 ? (<dl className="vars">
            {modules.map(function (_a) {
                    var _b = tslib_1.__read(_a, 2), key = _b[0], value = _b[1];
                    return (<react_1.Fragment key={key}>
                <dt>{key}</dt>
                <dd>
                  <pre className="val">{value}</pre>
                </dd>
              </react_1.Fragment>);
                })}
          </dl>) : (<p>{locale_1.t('No modules registered')}</p>)}
      </div>);
    };
    return AdminPackages;
}(asyncView_1.default));
exports.default = AdminPackages;
//# sourceMappingURL=adminPackages.jsx.map