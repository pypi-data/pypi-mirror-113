Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var form_1 = tslib_1.__importDefault(require("app/components/forms/form"));
var textField_1 = tslib_1.__importDefault(require("app/components/forms/textField"));
var locale_1 = require("app/locale");
var SsoForm = /** @class */ (function (_super) {
    tslib_1.__extends(SsoForm, _super);
    function SsoForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            errorMessage: null,
        };
        _this.handleSubmit = function (data, onSuccess, onError) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var api, response, e_1, message;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        api = this.props.api;
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise('/auth/sso-locate/', {
                                method: 'POST',
                                data: data,
                            })];
                    case 2:
                        response = _a.sent();
                        onSuccess(data);
                        react_router_1.browserHistory.push({ pathname: response.nextUri });
                        return [3 /*break*/, 4];
                    case 3:
                        e_1 = _a.sent();
                        if (!e_1.responseJSON) {
                            onError(e_1);
                            return [2 /*return*/];
                        }
                        message = e_1.responseJSON.detail;
                        this.setState({ errorMessage: message });
                        onError(e_1);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    SsoForm.prototype.render = function () {
        var serverHostname = this.props.authConfig.serverHostname;
        var errorMessage = this.state.errorMessage;
        return (<form_1.default className="form-stacked" submitLabel={locale_1.t('Continue')} onSubmit={this.handleSubmit} footerClass="auth-footer" errorMessage={errorMessage}>
        <textField_1.default name="organization" placeholder="acme" label={locale_1.t('Organization ID')} required help={locale_1.tct('Your ID is the slug after the hostname. e.g. [example] is [slug].', {
                slug: <strong>acme</strong>,
                example: <SlugExample slug="acme" hostname={serverHostname}/>,
            })}/>
      </form_1.default>);
    };
    return SsoForm;
}(react_1.Component));
var SlugExample = function (_a) {
    var hostname = _a.hostname, slug = _a.slug;
    return (<code>
    {hostname}/<strong>{slug}</strong>
  </code>);
};
exports.default = SsoForm;
//# sourceMappingURL=ssoForm.jsx.map