Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var mobx_react_1 = require("mobx-react");
var scroll_to_element_1 = tslib_1.__importDefault(require("scroll-to-element"));
var indicator_1 = require("app/actionCreators/indicator");
var sentryAppTokens_1 = require("app/actionCreators/sentryAppTokens");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var panels_1 = require("app/components/panels");
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var constants_1 = require("app/constants");
var sentryApplication_1 = require("app/data/forms/sentryApplication");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var formField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/formField"));
var jsonForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/jsonForm"));
var model_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/model"));
var textCopyInput_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/textCopyInput"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var permissionsObserver_1 = tslib_1.__importDefault(require("app/views/settings/organizationDeveloperSettings/permissionsObserver"));
/**
 * Finds the resource in SENTRY_APP_PERMISSIONS that contains a given scope
 * We should always find a match unless there is a bug
 * @param {Scope} scope
 * @return {Resource | undefined}
 */
var getResourceFromScope = function (scope) {
    var e_1, _a;
    try {
        for (var SENTRY_APP_PERMISSIONS_1 = tslib_1.__values(constants_1.SENTRY_APP_PERMISSIONS), SENTRY_APP_PERMISSIONS_1_1 = SENTRY_APP_PERMISSIONS_1.next(); !SENTRY_APP_PERMISSIONS_1_1.done; SENTRY_APP_PERMISSIONS_1_1 = SENTRY_APP_PERMISSIONS_1.next()) {
            var permObj = SENTRY_APP_PERMISSIONS_1_1.value;
            var allChoices = Object.values(permObj.choices);
            var allScopes = allChoices.reduce(function (_allScopes, choice) { var _a; return _allScopes.concat((_a = choice === null || choice === void 0 ? void 0 : choice.scopes) !== null && _a !== void 0 ? _a : []); }, []);
            if (allScopes.includes(scope)) {
                return permObj.resource;
            }
        }
    }
    catch (e_1_1) { e_1 = { error: e_1_1 }; }
    finally {
        try {
            if (SENTRY_APP_PERMISSIONS_1_1 && !SENTRY_APP_PERMISSIONS_1_1.done && (_a = SENTRY_APP_PERMISSIONS_1.return)) _a.call(SENTRY_APP_PERMISSIONS_1);
        }
        finally { if (e_1) throw e_1.error; }
    }
    return undefined;
};
var SentryAppFormModel = /** @class */ (function (_super) {
    tslib_1.__extends(SentryAppFormModel, _super);
    function SentryAppFormModel() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    /**
     * Filter out Permission input field values.
     *
     * Permissions (API Scopes) are presented as a list of SelectFields.
     * Instead of them being submitted individually, we want them rolled
     * up into a single list of scopes (this is done in `PermissionSelection`).
     *
     * Because they are all individual inputs, we end up with attributes
     * in the JSON we send to the API that we don't want.
     *
     * This function filters those attributes out of the data that is
     * ultimately sent to the API.
     */
    SentryAppFormModel.prototype.getData = function () {
        return this.fields.toJSON().reduce(function (data, _a) {
            var _b = tslib_1.__read(_a, 2), k = _b[0], v = _b[1];
            if (!k.endsWith('--permission')) {
                data[k] = v;
            }
            return data;
        }, {});
    };
    /**
     * We need to map the API response errors to the actual form fields.
     * We do this by pulling out scopes and mapping each scope error to the correct input.
     * @param {Object} responseJSON
     */
    SentryAppFormModel.prototype.mapFormErrors = function (responseJSON) {
        if (!responseJSON) {
            return responseJSON;
        }
        var formErrors = omit_1.default(responseJSON, ['scopes']);
        if (responseJSON.scopes) {
            responseJSON.scopes.forEach(function (message) {
                // find the scope from the error message of a specific format
                var matches = message.match(/Requested permission of (\w+:\w+)/);
                if (matches) {
                    var scope = matches[1];
                    var resource = getResourceFromScope(scope);
                    // should always match but technically resource can be undefined
                    if (resource) {
                        formErrors[resource + "--permission"] = [message];
                    }
                }
            });
        }
        return formErrors;
    };
    return SentryAppFormModel;
}(model_1.default));
var SentryApplicationDetails = /** @class */ (function (_super) {
    tslib_1.__extends(SentryApplicationDetails, _super);
    function SentryApplicationDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.form = new SentryAppFormModel();
        _this.handleSubmitSuccess = function (data) {
            var app = _this.state.app;
            var orgId = _this.props.params.orgId;
            var baseUrl = "/settings/" + orgId + "/developer-settings/";
            var url = app ? baseUrl : "" + baseUrl + data.slug + "/";
            if (app) {
                indicator_1.addSuccessMessage(locale_1.t('%s successfully saved.', data.name));
            }
            else {
                indicator_1.addSuccessMessage(locale_1.t('%s successfully created.', data.name));
            }
            react_router_1.browserHistory.push(url);
        };
        _this.handleSubmitError = function (err) {
            var _a;
            var errorMessage = locale_1.t('Unknown Error');
            if (err.status >= 400 && err.status < 500) {
                errorMessage = (_a = err === null || err === void 0 ? void 0 : err.responseJSON.detail) !== null && _a !== void 0 ? _a : errorMessage;
            }
            indicator_1.addErrorMessage(errorMessage);
            if (_this.form.formErrors) {
                var firstErrorFieldId = Object.keys(_this.form.formErrors)[0];
                if (firstErrorFieldId) {
                    scroll_to_element_1.default("#" + firstErrorFieldId, {
                        align: 'middle',
                        offset: 0,
                    });
                }
            }
        };
        _this.onAddToken = function (evt) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, app, tokens, api, token, newTokens;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        evt.preventDefault();
                        _a = this.state, app = _a.app, tokens = _a.tokens;
                        if (!app) {
                            return [2 /*return*/];
                        }
                        api = this.api;
                        return [4 /*yield*/, sentryAppTokens_1.addSentryAppToken(api, app)];
                    case 1:
                        token = _b.sent();
                        newTokens = tokens.concat(token);
                        this.setState({ tokens: newTokens });
                        return [2 /*return*/];
                }
            });
        }); };
        _this.onRemoveToken = function (token, evt) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, app, tokens, api, newTokens;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        evt.preventDefault();
                        _a = this.state, app = _a.app, tokens = _a.tokens;
                        if (!app) {
                            return [2 /*return*/];
                        }
                        api = this.api;
                        newTokens = tokens.filter(function (tok) { return tok.token !== token.token; });
                        return [4 /*yield*/, sentryAppTokens_1.removeSentryAppToken(api, app, token.token)];
                    case 1:
                        _b.sent();
                        this.setState({ tokens: newTokens });
                        return [2 /*return*/];
                }
            });
        }); };
        _this.renderTokens = function () {
            var tokens = _this.state.tokens;
            if (tokens.length > 0) {
                return tokens.map(function (token) { return (<StyledPanelItem key={token.token}>
          <TokenItem>
            <tooltip_1.default disabled={_this.showAuthInfo} position="right" containerDisplayMode="inline" title={locale_1.t('You do not have access to view these credentials because the permissions for this integration exceed those of your role.')}>
              <textCopyInput_1.default>
                {getDynamicText_1.default({ value: token.token, fixed: 'xxxxxx' })}
              </textCopyInput_1.default>
            </tooltip_1.default>
          </TokenItem>
          <CreatedDate>
            <CreatedTitle>Created:</CreatedTitle>
            <dateTime_1.default date={getDynamicText_1.default({
                        value: token.dateCreated,
                        fixed: new Date(1508208080000),
                    })}/>
          </CreatedDate>
          <button_1.default onClick={_this.onRemoveToken.bind(_this, token)} size="small" icon={<icons_1.IconDelete />} data-test-id="token-delete" type="button">
            {locale_1.t('Revoke')}
          </button_1.default>
        </StyledPanelItem>); });
            }
            else {
                return <emptyMessage_1.default description={locale_1.t('No tokens created yet.')}/>;
            }
        };
        _this.onFieldChange = function (name, value) {
            if (name === 'webhookUrl' && !value && _this.isInternal) {
                // if no webhook, then set isAlertable to false
                _this.form.setValue('isAlertable', false);
            }
        };
        return _this;
    }
    SentryApplicationDetails.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { app: null, tokens: [] });
    };
    SentryApplicationDetails.prototype.getEndpoints = function () {
        var appSlug = this.props.params.appSlug;
        if (appSlug) {
            return [
                ['app', "/sentry-apps/" + appSlug + "/"],
                ['tokens', "/sentry-apps/" + appSlug + "/api-tokens/"],
            ];
        }
        return [];
    };
    SentryApplicationDetails.prototype.getTitle = function () {
        var orgId = this.props.params.orgId;
        return routeTitle_1.default(locale_1.t('Sentry Integration Details'), orgId, false);
    };
    // Events may come from the API as "issue.created" when we just want "issue" here.
    SentryApplicationDetails.prototype.normalize = function (events) {
        if (events.length === 0) {
            return events;
        }
        return events.map(function (e) { return e.split('.').shift(); });
    };
    Object.defineProperty(SentryApplicationDetails.prototype, "isInternal", {
        get: function () {
            var app = this.state.app;
            if (app) {
                // if we are editing an existing app, check the status of the app
                return app.status === 'internal';
            }
            return this.props.route.path === 'new-internal/';
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(SentryApplicationDetails.prototype, "showAuthInfo", {
        get: function () {
            var app = this.state.app;
            return !(app && app.clientSecret && app.clientSecret[0] === '*');
        },
        enumerable: false,
        configurable: true
    });
    SentryApplicationDetails.prototype.renderBody = function () {
        var _this = this;
        var orgId = this.props.params.orgId;
        var app = this.state.app;
        var scopes = (app && tslib_1.__spreadArray([], tslib_1.__read(app.scopes))) || [];
        var events = (app && this.normalize(app.events)) || [];
        var method = app ? 'PUT' : 'POST';
        var endpoint = app ? "/sentry-apps/" + app.slug + "/" : '/sentry-apps/';
        var forms = this.isInternal ? sentryApplication_1.internalIntegrationForms : sentryApplication_1.publicIntegrationForms;
        var verifyInstall;
        if (this.isInternal) {
            // force verifyInstall to false for all internal apps
            verifyInstall = false;
        }
        else {
            // use the existing value for verifyInstall if the app exists, otherwise default to true
            verifyInstall = app ? app.verifyInstall : true;
        }
        return (<div>
        <settingsPageHeader_1.default title={this.getTitle()}/>
        <form_1.default apiMethod={method} apiEndpoint={endpoint} allowUndo initialData={tslib_1.__assign(tslib_1.__assign({ organization: orgId, isAlertable: false, isInternal: this.isInternal, schema: {}, scopes: [] }, app), { verifyInstall: verifyInstall })} model={this.form} onSubmitSuccess={this.handleSubmitSuccess} onSubmitError={this.handleSubmitError} onFieldChange={this.onFieldChange}>
          <mobx_react_1.Observer>
            {function () {
                var webhookDisabled = _this.isInternal && !_this.form.getValue('webhookUrl');
                return (<React.Fragment>
                  <jsonForm_1.default additionalFieldProps={{ webhookDisabled: webhookDisabled }} forms={forms}/>

                  <permissionsObserver_1.default webhookDisabled={webhookDisabled} appPublished={app ? app.status === 'published' : false} scopes={scopes} events={events}/>
                </React.Fragment>);
            }}
          </mobx_react_1.Observer>

          {app && app.status === 'internal' && (<panels_1.Panel>
              <panels_1.PanelHeader hasButtons>
                {locale_1.t('Tokens')}
                <button_1.default size="xsmall" icon={<icons_1.IconAdd size="xs" isCircled/>} onClick={function (evt) { return _this.onAddToken(evt); }} data-test-id="token-add" type="button">
                  {locale_1.t('New Token')}
                </button_1.default>
              </panels_1.PanelHeader>
              <panels_1.PanelBody>{this.renderTokens()}</panels_1.PanelBody>
            </panels_1.Panel>)}

          {app && (<panels_1.Panel>
              <panels_1.PanelHeader>{locale_1.t('Credentials')}</panels_1.PanelHeader>
              <panels_1.PanelBody>
                {app.status !== 'internal' && (<formField_1.default name="clientId" label="Client ID">
                    {function (_a) {
                        var value = _a.value;
                        return (<textCopyInput_1.default>
                        {getDynamicText_1.default({ value: value, fixed: 'CI_CLIENT_ID' })}
                      </textCopyInput_1.default>);
                    }}
                  </formField_1.default>)}
                <formField_1.default name="clientSecret" label="Client Secret">
                  {function (_a) {
                    var value = _a.value;
                    return value ? (<tooltip_1.default disabled={_this.showAuthInfo} position="right" containerDisplayMode="inline" title={locale_1.t('You do not have access to view these credentials because the permissions for this integration exceed those of your role.')}>
                        <textCopyInput_1.default>
                          {getDynamicText_1.default({ value: value, fixed: 'CI_CLIENT_SECRET' })}
                        </textCopyInput_1.default>
                      </tooltip_1.default>) : (<em>hidden</em>);
                }}
                </formField_1.default>
              </panels_1.PanelBody>
            </panels_1.Panel>)}
        </form_1.default>
      </div>);
    };
    return SentryApplicationDetails;
}(asyncView_1.default));
exports.default = SentryApplicationDetails;
var StyledPanelItem = styled_1.default(panels_1.PanelItem)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  justify-content: space-between;\n"], ["\n  display: flex;\n  justify-content: space-between;\n"])));
var TokenItem = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  width: 70%;\n"], ["\n  width: 70%;\n"])));
var CreatedTitle = styled_1.default('span')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  margin-bottom: 2px;\n"], ["\n  color: ", ";\n  margin-bottom: 2px;\n"])), function (p) { return p.theme.gray300; });
var CreatedDate = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  font-size: 14px;\n  margin: 0 10px;\n"], ["\n  display: flex;\n  flex-direction: column;\n  font-size: 14px;\n  margin: 0 10px;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=sentryApplicationDetails.jsx.map