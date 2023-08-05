Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var indicator_1 = require("app/actionCreators/indicator");
var api_1 = require("app/api");
var form_1 = tslib_1.__importDefault(require("app/components/forms/form"));
var formField_1 = tslib_1.__importDefault(require("app/components/forms/formField"));
var state_1 = tslib_1.__importDefault(require("app/components/forms/state"));
var locale_1 = require("app/locale");
var ApiForm = /** @class */ (function (_super) {
    tslib_1.__extends(ApiForm, _super);
    function ApiForm() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.api = new api_1.Client();
        _this.onSubmit = function (e) {
            e.preventDefault();
            if (_this.state.state === state_1.default.SAVING) {
                return;
            }
            // Actual HTML forms do not submit data for disabled fields, and because of
            // the way some of our APIs are implemented, we need to start doing the
            // same. But, since some other parts of the app very probably depend on
            // sending disabled fields, keep that the default for now.
            // TODO(chadwhitacre): Expand and upstream this.
            var data = _this.props.omitDisabled ? _this.getEnabledData() : _this.state.data;
            _this.props.onSubmit && _this.props.onSubmit(data);
            _this.setState({
                state: state_1.default.SAVING,
            }, function () {
                indicator_1.addLoadingMessage(_this.props.submitLoadingMessage);
                _this.api.request(_this.props.apiEndpoint, {
                    method: _this.props.apiMethod,
                    data: data,
                    success: function (result) {
                        indicator_1.clearIndicators();
                        _this.onSubmitSuccess(result);
                    },
                    error: function (error) {
                        indicator_1.addErrorMessage(_this.props.submitErrorMessage);
                        _this.onSubmitError(error);
                    },
                });
            });
        };
        return _this;
    }
    ApiForm.prototype.componentWillUnmount = function () {
        this.api.clear();
    };
    ApiForm.prototype.getEnabledData = function () {
        // Return a hash of data from non-disabled fields.
        // Start with this.state.data and remove rather than starting from scratch
        // and adding, because a) this.state.data is our source of truth, and b)
        // we'd have to do more work to loop over the state.data Object and lookup
        // against the props.children Array (looping over the Array and looking up
        // in the Object is more natural). Maybe the consequent use of delete
        // carries a slight performance hit. Why is yer form so big? 🤔
        var data = tslib_1.__assign({}, this.state.data); // Copy to avoid mutating state.data itself.
        React.Children.forEach(this.props.children, function (child) {
            var _a;
            if (!formField_1.default.isPrototypeOf(child.type)) {
                return; // Form children include h4's, etc.
            }
            if (child.key && ((_a = child.props) === null || _a === void 0 ? void 0 : _a.disabled)) {
                delete data[child.key]; // Assume a link between child.key and data. 🐭
            }
        });
        return data;
    };
    ApiForm.defaultProps = tslib_1.__assign(tslib_1.__assign({}, form_1.default.defaultProps), { omitDisabled: false, submitErrorMessage: locale_1.t('There was an error saving your changes.'), submitLoadingMessage: locale_1.t('Saving changes\u2026') });
    return ApiForm;
}(form_1.default));
exports.default = ApiForm;
//# sourceMappingURL=apiForm.jsx.map