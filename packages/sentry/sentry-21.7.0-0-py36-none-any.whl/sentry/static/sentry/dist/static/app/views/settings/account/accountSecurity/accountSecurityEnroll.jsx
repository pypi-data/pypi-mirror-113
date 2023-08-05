Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var qrcode_react_1 = tslib_1.__importDefault(require("qrcode.react"));
var indicator_1 = require("app/actionCreators/indicator");
var modal_1 = require("app/actionCreators/modal");
var organizations_1 = require("app/actionCreators/organizations");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var circleIndicator_1 = tslib_1.__importDefault(require("app/components/circleIndicator"));
var panels_1 = require("app/components/panels");
var u2fsign_1 = tslib_1.__importDefault(require("app/components/u2f/u2fsign"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var getPendingInvite_1 = tslib_1.__importDefault(require("app/utils/getPendingInvite"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var removeConfirm_1 = tslib_1.__importDefault(require("app/views/settings/account/accountSecurity/components/removeConfirm"));
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var jsonForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/jsonForm"));
var model_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/model"));
var textCopyInput_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/textCopyInput"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
/**
 * Retrieve additional form fields (or modify ones) based on 2fa method
 */
var getFields = function (_a) {
    var authenticator = _a.authenticator, hasSentCode = _a.hasSentCode, sendingCode = _a.sendingCode, onSmsReset = _a.onSmsReset, onU2fTap = _a.onU2fTap;
    var form = authenticator.form;
    if (!form) {
        return null;
    }
    if (authenticator.id === 'totp') {
        return tslib_1.__spreadArray(tslib_1.__spreadArray([
            function () { return (<CodeContainer key="qrcode">
          <StyledQRCode value={authenticator.qrcode} size={228}/>
        </CodeContainer>); },
            function () {
                var _a;
                return (<field_1.default key="secret" label={locale_1.t('Authenticator secret')}>
          <textCopyInput_1.default>{(_a = authenticator.secret) !== null && _a !== void 0 ? _a : ''}</textCopyInput_1.default>
        </field_1.default>);
            }
        ], tslib_1.__read(form)), [
            function () { return (<Actions key="confirm">
          <button_1.default priority="primary" type="submit">
            {locale_1.t('Confirm')}
          </button_1.default>
        </Actions>); },
        ]);
    }
    // Sms Form needs a start over button + confirm button
    // Also inputs being disabled vary based on hasSentCode
    if (authenticator.id === 'sms') {
        // Ideally we would have greater flexibility when rendering footer
        return tslib_1.__spreadArray(tslib_1.__spreadArray([
            tslib_1.__assign(tslib_1.__assign({}, form[0]), { disabled: sendingCode || hasSentCode })
        ], tslib_1.__read((hasSentCode ? [tslib_1.__assign(tslib_1.__assign({}, form[1]), { required: true })] : []))), [
            function () { return (<Actions key="sms-footer">
          <buttonBar_1.default gap={1}>
            {hasSentCode && <button_1.default onClick={onSmsReset}>{locale_1.t('Start Over')}</button_1.default>}
            <button_1.default priority="primary" type="submit">
              {hasSentCode ? locale_1.t('Confirm') : locale_1.t('Send Code')}
            </button_1.default>
          </buttonBar_1.default>
        </Actions>); },
        ]);
    }
    // Need to render device name field + U2f component
    if (authenticator.id === 'u2f') {
        var deviceNameField = form.find(function (_a) {
            var name = _a.name;
            return name === 'deviceName';
        });
        return [
            deviceNameField,
            function () { return (<u2fsign_1.default key="u2f-enroll" style={{ marginBottom: 0 }} challengeData={authenticator.challenge} displayMode="enroll" onTap={onU2fTap}/>); },
        ];
    }
    return null;
};
/**
 * Renders necessary forms in order to enroll user in 2fa
 */
var AccountSecurityEnroll = /** @class */ (function (_super) {
    tslib_1.__extends(AccountSecurityEnroll, _super);
    function AccountSecurityEnroll() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.formModel = new model_1.default();
        _this.pendingInvitation = null;
        // This resets state so that user can re-enter their phone number again
        _this.handleSmsReset = function () { return _this.setState({ hasSentCode: false }, _this.remountComponent); };
        // Handles SMS authenticators
        _this.handleSmsSubmit = function (dataModel) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, authenticator, hasSentCode, phone, otp, data, error_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.state, authenticator = _a.authenticator, hasSentCode = _a.hasSentCode;
                        phone = dataModel.phone, otp = dataModel.otp;
                        // Don't submit if empty
                        if (!phone || !authenticator) {
                            return [2 /*return*/];
                        }
                        data = {
                            phone: phone,
                            // Make sure `otp` is undefined if we are submitting OTP verification
                            // Otherwise API will think that we are on verification step (e.g. after submitting phone)
                            otp: hasSentCode ? otp : undefined,
                            secret: authenticator.secret,
                        };
                        // Only show loading when submitting OTP
                        this.setState({ sendingCode: !hasSentCode });
                        if (!hasSentCode) {
                            indicator_1.addLoadingMessage(locale_1.t('Sending code to %s...', data.phone));
                        }
                        else {
                            indicator_1.addLoadingMessage(locale_1.t('Verifying OTP...'));
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise(this.enrollEndpoint, { data: data })];
                    case 2:
                        _b.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        this.formModel.resetForm();
                        indicator_1.addErrorMessage(this.state.hasSentCode ? locale_1.t('Incorrect OTP') : locale_1.t('Error sending SMS'));
                        this.setState({
                            hasSentCode: false,
                            sendingCode: false,
                        });
                        // Re-mount because we want to fetch a fresh secret
                        this.remountComponent();
                        return [2 /*return*/];
                    case 4:
                        if (!hasSentCode) {
                            // Just successfully finished sending OTP to user
                            this.setState({ hasSentCode: true, sendingCode: false });
                            indicator_1.addSuccessMessage(locale_1.t('Sent code to %s', data.phone));
                        }
                        else {
                            // OTP was accepted and SMS was added as a 2fa method
                            this.handleEnrollSuccess();
                        }
                        return [2 /*return*/];
                }
            });
        }); };
        // Handle u2f device tap
        _this.handleU2fTap = function (tapData) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var data, err_1;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        data = tslib_1.__assign({ deviceName: this.formModel.getValue('deviceName') }, tapData);
                        this.setState({ loading: true });
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise(this.enrollEndpoint, { data: data })];
                    case 2:
                        _a.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _a.sent();
                        this.handleEnrollError();
                        return [2 /*return*/];
                    case 4:
                        this.handleEnrollSuccess();
                        return [2 /*return*/];
                }
            });
        }); };
        // Currently only TOTP uses this
        _this.handleTotpSubmit = function (dataModel) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var data, err_2;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (!this.state.authenticator) {
                            return [2 /*return*/];
                        }
                        data = tslib_1.__assign(tslib_1.__assign({}, (dataModel !== null && dataModel !== void 0 ? dataModel : {})), { secret: this.state.authenticator.secret });
                        this.setState({ loading: true });
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise(this.enrollEndpoint, { method: 'POST', data: data })];
                    case 2:
                        _a.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        err_2 = _a.sent();
                        this.handleEnrollError();
                        return [2 /*return*/];
                    case 4:
                        this.handleEnrollSuccess();
                        return [2 /*return*/];
                }
            });
        }); };
        _this.handleSubmit = function (data) {
            var _a;
            var id = (_a = _this.state.authenticator) === null || _a === void 0 ? void 0 : _a.id;
            if (id === 'totp') {
                _this.handleTotpSubmit(data);
                return;
            }
            if (id === 'sms') {
                _this.handleSmsSubmit(data);
                return;
            }
        };
        // Removes an authenticator
        _this.handleRemove = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var authenticator, err_3;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        authenticator = this.state.authenticator;
                        if (!authenticator || !authenticator.authId) {
                            return [2 /*return*/];
                        }
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise(this.authenticatorEndpoint, { method: 'DELETE' })];
                    case 2:
                        _a.sent();
                        return [3 /*break*/, 4];
                    case 3:
                        err_3 = _a.sent();
                        indicator_1.addErrorMessage(locale_1.t('Error removing authenticator'));
                        return [2 /*return*/];
                    case 4:
                        this.props.router.push('/settings/account/security/');
                        indicator_1.addSuccessMessage(locale_1.t('Authenticator has been removed'));
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    AccountSecurityEnroll.prototype.getTitle = function () {
        return locale_1.t('Security');
    };
    AccountSecurityEnroll.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { hasSentCode: false });
    };
    Object.defineProperty(AccountSecurityEnroll.prototype, "authenticatorEndpoint", {
        get: function () {
            return "/users/me/authenticators/" + this.props.params.authId + "/";
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(AccountSecurityEnroll.prototype, "enrollEndpoint", {
        get: function () {
            return this.authenticatorEndpoint + "enroll/";
        },
        enumerable: false,
        configurable: true
    });
    AccountSecurityEnroll.prototype.getEndpoints = function () {
        var _this = this;
        var errorHandler = function (err) {
            var alreadyEnrolled = err &&
                err.status === 400 &&
                err.responseJSON &&
                err.responseJSON.details === 'Already enrolled';
            if (alreadyEnrolled) {
                _this.props.router.push('/settings/account/security/');
                indicator_1.addErrorMessage(locale_1.t('Already enrolled'));
            }
            // Allow the endpoint to fail if the user is already enrolled
            return alreadyEnrolled;
        };
        return [['authenticator', this.enrollEndpoint, {}, { allowError: errorHandler }]];
    };
    AccountSecurityEnroll.prototype.componentDidMount = function () {
        this.pendingInvitation = getPendingInvite_1.default();
    };
    Object.defineProperty(AccountSecurityEnroll.prototype, "authenticatorName", {
        get: function () {
            var _a, _b;
            return (_b = (_a = this.state.authenticator) === null || _a === void 0 ? void 0 : _a.name) !== null && _b !== void 0 ? _b : 'Authenticator';
        },
        enumerable: false,
        configurable: true
    });
    // Handler when we successfully add a 2fa device
    AccountSecurityEnroll.prototype.handleEnrollSuccess = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (!this.pendingInvitation) return [3 /*break*/, 2];
                        return [4 /*yield*/, organizations_1.fetchOrganizationByMember(this.pendingInvitation.memberId.toString(), {
                                addOrg: true,
                                fetchOrgDetails: true,
                            })];
                    case 1:
                        _a.sent();
                        _a.label = 2;
                    case 2:
                        this.props.router.push('/settings/account/security/');
                        modal_1.openRecoveryOptions({ authenticatorName: this.authenticatorName });
                        return [2 /*return*/];
                }
            });
        });
    };
    // Handler when we failed to add a 2fa device
    AccountSecurityEnroll.prototype.handleEnrollError = function () {
        this.setState({ loading: false });
        indicator_1.addErrorMessage(locale_1.t('Error adding %s authenticator', this.authenticatorName));
    };
    AccountSecurityEnroll.prototype.renderBody = function () {
        var _a;
        var _b = this.state, authenticator = _b.authenticator, hasSentCode = _b.hasSentCode, sendingCode = _b.sendingCode;
        if (!authenticator) {
            return null;
        }
        var fields = getFields({
            authenticator: authenticator,
            hasSentCode: hasSentCode,
            sendingCode: sendingCode,
            onSmsReset: this.handleSmsReset,
            onU2fTap: this.handleU2fTap,
        });
        // Attempt to extract `defaultValue` from server generated form fields
        var defaultValues = fields
            ? fields
                .filter(function (field) {
                return typeof field !== 'function' && typeof field.defaultValue !== 'undefined';
            })
                .map(function (field) { return [
                field.name,
                typeof field !== 'function' ? field.defaultValue : '',
            ]; })
                .reduce(function (acc, _a) {
                var _b = tslib_1.__read(_a, 2), name = _b[0], value = _b[1];
                acc[name] = value;
                return acc;
            }, {})
            : {};
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title={<react_1.Fragment>
              <span>{authenticator.name}</span>
              <circleIndicator_1.default css={{ marginLeft: 6 }} enabled={authenticator.isEnrolled}/>
            </react_1.Fragment>} action={authenticator.isEnrolled &&
                authenticator.removeButton && (<removeConfirm_1.default onConfirm={this.handleRemove}>
                <button_1.default priority="danger">{authenticator.removeButton}</button_1.default>
              </removeConfirm_1.default>)}/>

        <textBlock_1.default>{authenticator.description}</textBlock_1.default>

        {!!((_a = authenticator.form) === null || _a === void 0 ? void 0 : _a.length) && (<form_1.default model={this.formModel} apiMethod="POST" apiEndpoint={this.authenticatorEndpoint} onSubmit={this.handleSubmit} initialData={tslib_1.__assign(tslib_1.__assign({}, defaultValues), authenticator)} hideFooter>
            <jsonForm_1.default forms={[{ title: 'Configuration', fields: fields !== null && fields !== void 0 ? fields : [] }]}/>
          </form_1.default>)}
      </react_1.Fragment>);
    };
    return AccountSecurityEnroll;
}(asyncView_1.default));
var CodeContainer = styled_1.default(panels_1.PanelItem)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  justify-content: center;\n"], ["\n  justify-content: center;\n"])));
var Actions = styled_1.default(panels_1.PanelItem)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  justify-content: flex-end;\n"], ["\n  justify-content: flex-end;\n"])));
var StyledQRCode = styled_1.default(qrcode_react_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  background: white;\n  padding: ", ";\n"], ["\n  background: white;\n  padding: ", ";\n"])), space_1.default(2));
exports.default = react_router_1.withRouter(AccountSecurityEnroll);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=accountSecurityEnroll.jsx.map