Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var moment_1 = tslib_1.__importDefault(require("moment"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var AdminEnvironment = /** @class */ (function (_super) {
    tslib_1.__extends(AdminEnvironment, _super);
    function AdminEnvironment() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    AdminEnvironment.prototype.getEndpoints = function () {
        return [['data', '/internal/environment/']];
    };
    AdminEnvironment.prototype.renderBody = function () {
        var data = this.state.data;
        var environment = data.environment, config = data.config, pythonVersion = data.pythonVersion;
        var version = configStore_1.default.getConfig().version;
        return (<div>
        <h3>{locale_1.t('Environment')}</h3>

        {environment ? (<dl className="vars">
            <VersionLabel>
              {locale_1.t('Server Version')}
              {version.upgradeAvailable && (<button_1.default title={locale_1.t("You're running an old version of Sentry, did you know %s is available?", version.latest)} priority="link" href="https://github.com/getsentry/sentry/releases" icon={<icons_1.IconQuestion size="sm"/>} size="small" external/>)}
            </VersionLabel>
            <dd>
              <pre className="val">{version.current}</pre>
            </dd>

            <dt>{locale_1.t('Python Version')}</dt>
            <dd>
              <pre className="val">{pythonVersion}</pre>
            </dd>
            <dt>{locale_1.t('Configuration File')}</dt>
            <dd>
              <pre className="val">{environment.config}</pre>
            </dd>
            <dt>{locale_1.t('Uptime')}</dt>
            <dd>
              <pre className="val">
                {moment_1.default(environment.start_date).toNow(true)} (since{' '}
                {environment.start_date})
              </pre>
            </dd>
          </dl>) : (<p>
            {locale_1.t('Environment not found (are you using the builtin Sentry webserver?).')}
          </p>)}

        <h3>
          {locale_1.tct('Configuration [configPath]', {
                configPath: environment.config && <small>{environment.config}</small>,
            })}
        </h3>

        <dl className="vars">
          {config.map(function (_a) {
                var _b = tslib_1.__read(_a, 2), key = _b[0], value = _b[1];
                return (<react_1.Fragment key={key}>
              <dt>{key}</dt>
              <dd>
                <pre className="val">{value}</pre>
              </dd>
            </react_1.Fragment>);
            })}
        </dl>
      </div>);
    };
    return AdminEnvironment;
}(asyncView_1.default));
exports.default = AdminEnvironment;
var VersionLabel = styled_1.default('dt')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n"], ["\n  display: inline-grid;\n  grid-auto-flow: column;\n  grid-gap: ", ";\n  align-items: center;\n"])), space_1.default(1));
var templateObject_1;
//# sourceMappingURL=adminEnvironment.jsx.map