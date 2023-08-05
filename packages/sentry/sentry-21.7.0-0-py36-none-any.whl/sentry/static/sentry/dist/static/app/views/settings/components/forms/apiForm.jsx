Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var indicator_1 = require("app/actionCreators/indicator");
var api_1 = require("app/api");
var locale_1 = require("app/locale");
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var ApiForm = /** @class */ (function (_super) {
    tslib_1.__extends(ApiForm, _super);
    function ApiForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.api = new api_1.Client();
        _this.onSubmit = function (data, onSuccess, onError) {
            _this.props.onSubmit && _this.props.onSubmit(data);
            indicator_1.addLoadingMessage(locale_1.t('Saving changes\u2026'));
            _this.api.request(_this.props.apiEndpoint, {
                method: _this.props.apiMethod,
                data: data,
                success: function (response) {
                    indicator_1.clearIndicators();
                    onSuccess(response);
                },
                error: function (error) {
                    indicator_1.clearIndicators();
                    onError(error);
                },
            });
        };
        return _this;
    }
    ApiForm.prototype.componentWillUnmount = function () {
        this.api.clear();
    };
    ApiForm.prototype.render = function () {
        var _a = this.props, _onSubmit = _a.onSubmit, _apiMethod = _a.apiMethod, _apiEndpoint = _a.apiEndpoint, otherProps = tslib_1.__rest(_a, ["onSubmit", "apiMethod", "apiEndpoint"]);
        return <form_1.default onSubmit={this.onSubmit} {...otherProps}/>;
    };
    return ApiForm;
}(react_1.Component));
exports.default = ApiForm;
//# sourceMappingURL=apiForm.jsx.map