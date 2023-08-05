Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var indicator_1 = require("app/actionCreators/indicator");
var locale_1 = require("app/locale");
var form_1 = tslib_1.__importDefault(require("./form"));
var handleXhrErrorResponse_1 = tslib_1.__importDefault(require("./handleXhrErrorResponse"));
var modal_1 = tslib_1.__importDefault(require("./modal"));
var DialogManager = /** @class */ (function (_super) {
    tslib_1.__extends(DialogManager, _super);
    function DialogManager() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = _this.getDefaultState();
        _this.handleChange = function (field, value) {
            _this.setState(function (prevState) {
                var _a;
                return ({
                    values: tslib_1.__assign(tslib_1.__assign({}, prevState.values), (_a = {}, _a[field] = value, _a)),
                    errors: omit_1.default(prevState.errors, field),
                });
            });
        };
        _this.handleSave = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, onSubmitSuccess, closeModal, orgSlug, api, trustedRelays, response, error_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, onSubmitSuccess = _a.onSubmitSuccess, closeModal = _a.closeModal, orgSlug = _a.orgSlug, api = _a.api;
                        trustedRelays = this.getData().trustedRelays.map(function (trustedRelay) {
                            return omit_1.default(trustedRelay, ['created', 'lastModified']);
                        });
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/organizations/" + orgSlug + "/", {
                                method: 'PUT',
                                data: { trustedRelays: trustedRelays },
                            })];
                    case 2:
                        response = _b.sent();
                        onSubmitSuccess(response);
                        closeModal();
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        this.convertErrorXhrResponse(handleXhrErrorResponse_1.default(error_1));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleValidate = function (field) {
            return function () {
                var isFieldValueEmpty = !_this.state.values[field].replace(/\s/g, '');
                var fieldErrorAlreadyExist = _this.state.errors[field];
                if (isFieldValueEmpty && fieldErrorAlreadyExist) {
                    return;
                }
                if (isFieldValueEmpty && !fieldErrorAlreadyExist) {
                    _this.setState(function (prevState) {
                        var _a;
                        return ({
                            errors: tslib_1.__assign(tslib_1.__assign({}, prevState.errors), (_a = {}, _a[field] = locale_1.t('Field Required'), _a)),
                        });
                    });
                    return;
                }
                if (!isFieldValueEmpty && fieldErrorAlreadyExist) {
                    _this.clearError(field);
                }
            };
        };
        _this.handleValidateKey = function () {
            var savedRelays = _this.props.savedRelays;
            var _a = _this.state, values = _a.values, errors = _a.errors;
            var isKeyAlreadyTaken = savedRelays.find(function (savedRelay) { return savedRelay.publicKey === values.publicKey; });
            if (isKeyAlreadyTaken && !errors.publicKey) {
                _this.setState({
                    errors: tslib_1.__assign(tslib_1.__assign({}, errors), { publicKey: locale_1.t('Relay key already taken') }),
                });
                return;
            }
            if (errors.publicKey) {
                _this.setState({
                    errors: omit_1.default(errors, 'publicKey'),
                });
            }
            _this.handleValidate('publicKey')();
        };
        return _this;
    }
    DialogManager.prototype.componentDidMount = function () {
        this.validateForm();
    };
    DialogManager.prototype.componentDidUpdate = function (_prevProps, prevState) {
        if (!isEqual_1.default(prevState.values, this.state.values)) {
            this.validateForm();
        }
        if (!isEqual_1.default(prevState.errors, this.state.errors) &&
            Object.keys(this.state.errors).length > 0) {
            this.setValidForm(false);
        }
    };
    DialogManager.prototype.getDefaultState = function () {
        return {
            values: { name: '', publicKey: '', description: '' },
            requiredValues: ['name', 'publicKey'],
            errors: {},
            disables: {},
            isFormValid: false,
            title: this.getTitle(),
        };
    };
    DialogManager.prototype.getTitle = function () {
        return '';
    };
    DialogManager.prototype.getData = function () {
        // Child has to implement this
        throw new Error('Not implemented');
    };
    DialogManager.prototype.getBtnSaveLabel = function () {
        return undefined;
    };
    DialogManager.prototype.setValidForm = function (isFormValid) {
        this.setState({ isFormValid: isFormValid });
    };
    DialogManager.prototype.validateForm = function () {
        var _a = this.state, values = _a.values, requiredValues = _a.requiredValues, errors = _a.errors;
        var isFormValid = requiredValues.every(function (requiredValue) {
            return !!values[requiredValue].replace(/\s/g, '') && !errors[requiredValue];
        });
        this.setValidForm(isFormValid);
    };
    DialogManager.prototype.clearError = function (field) {
        this.setState(function (prevState) { return ({
            errors: omit_1.default(prevState.errors, field),
        }); });
    };
    DialogManager.prototype.convertErrorXhrResponse = function (error) {
        switch (error.type) {
            case 'invalid-key':
            case 'missing-key':
                this.setState(function (prevState) { return ({
                    errors: tslib_1.__assign(tslib_1.__assign({}, prevState.errors), { publicKey: error.message }),
                }); });
                break;
            case 'empty-name':
            case 'missing-name':
                this.setState(function (prevState) { return ({
                    errors: tslib_1.__assign(tslib_1.__assign({}, prevState.errors), { name: error.message }),
                }); });
                break;
            default:
                indicator_1.addErrorMessage(error.message);
        }
    };
    DialogManager.prototype.getForm = function () {
        var _a = this.state, values = _a.values, errors = _a.errors, disables = _a.disables, isFormValid = _a.isFormValid;
        return (<form_1.default isFormValid={isFormValid} onSave={this.handleSave} onChange={this.handleChange} onValidate={this.handleValidate} onValidateKey={this.handleValidateKey} errors={errors} values={values} disables={disables}/>);
    };
    DialogManager.prototype.getContent = function () {
        return this.getForm();
    };
    DialogManager.prototype.render = function () {
        var _a = this.state, title = _a.title, isFormValid = _a.isFormValid;
        var btnSaveLabel = this.getBtnSaveLabel();
        var content = this.getContent();
        return (<modal_1.default {...this.props} title={title} onSave={this.handleSave} btnSaveLabel={btnSaveLabel} disabled={!isFormValid} content={content}/>);
    };
    return DialogManager;
}(React.Component));
exports.default = DialogManager;
//# sourceMappingURL=modalManager.jsx.map