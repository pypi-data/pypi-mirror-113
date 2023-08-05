Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var alertLink_1 = tslib_1.__importDefault(require("app/components/alertLink"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var utils_1 = require("app/components/projects/appStoreConnectContext/utils");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var stepFifth_1 = tslib_1.__importDefault(require("./stepFifth"));
var stepFour_1 = tslib_1.__importDefault(require("./stepFour"));
var stepOne_1 = tslib_1.__importDefault(require("./stepOne"));
var stepThree_1 = tslib_1.__importDefault(require("./stepThree"));
var stepTwo_1 = tslib_1.__importDefault(require("./stepTwo"));
var steps = [
    locale_1.t('App Store Connect credentials'),
    locale_1.t('Choose an application'),
    locale_1.t('Enter iTunes credentials'),
    locale_1.t('Enter authentication code'),
    locale_1.t('Choose an organization'),
];
function AppStoreConnect(_a) {
    var Header = _a.Header, Body = _a.Body, Footer = _a.Footer, api = _a.api, initialData = _a.initialData, orgSlug = _a.orgSlug, projectSlug = _a.projectSlug, onSubmit = _a.onSubmit, location = _a.location, appStoreConnectContext = _a.appStoreConnectContext;
    var updateAlertMessage = (appStoreConnectContext !== null && appStoreConnectContext !== void 0 ? appStoreConnectContext : {}).updateAlertMessage;
    var _b = tslib_1.__read(react_1.useState(location.query.revalidateItunesSession), 2), revalidateItunesSession = _b[0], setRevalidateItunesSession = _b[1];
    var _c = tslib_1.__read(react_1.useState(false), 2), isLoading = _c[0], setIsLoading = _c[1];
    var _d = tslib_1.__read(react_1.useState(revalidateItunesSession ? 3 : 0), 2), activeStep = _d[0], setActiveStep = _d[1];
    var _e = tslib_1.__read(react_1.useState([]), 2), appStoreApps = _e[0], setAppStoreApps = _e[1];
    var _f = tslib_1.__read(react_1.useState([]), 2), appleStoreOrgs = _f[0], setAppleStoreOrgs = _f[1];
    var _g = tslib_1.__read(react_1.useState(false), 2), useSms = _g[0], setUseSms = _g[1];
    var _h = tslib_1.__read(react_1.useState(undefined), 2), sessionContext = _h[0], setSessionContext = _h[1];
    var _j = tslib_1.__read(react_1.useState({
        issuer: initialData === null || initialData === void 0 ? void 0 : initialData.appconnectIssuer,
        keyId: initialData === null || initialData === void 0 ? void 0 : initialData.appconnectKey,
        privateKey: initialData === null || initialData === void 0 ? void 0 : initialData.appconnectPrivateKey,
    }), 2), stepOneData = _j[0], setStepOneData = _j[1];
    var _k = tslib_1.__read(react_1.useState({
        app: (initialData === null || initialData === void 0 ? void 0 : initialData.appId) && (initialData === null || initialData === void 0 ? void 0 : initialData.appName)
            ? {
                appId: initialData.appId,
                name: initialData.appName,
                bundleId: initialData.bundleId,
            }
            : undefined,
    }), 2), stepTwoData = _k[0], setStepTwoData = _k[1];
    var _l = tslib_1.__read(react_1.useState({
        username: initialData === null || initialData === void 0 ? void 0 : initialData.itunesUser,
        password: initialData === null || initialData === void 0 ? void 0 : initialData.itunesPassword,
    }), 2), stepThreeData = _l[0], setStepThreeData = _l[1];
    var _m = tslib_1.__read(react_1.useState({
        authenticationCode: undefined,
    }), 2), stepFourData = _m[0], setStepFourData = _m[1];
    var _o = tslib_1.__read(react_1.useState({
        org: (initialData === null || initialData === void 0 ? void 0 : initialData.orgId) && (initialData === null || initialData === void 0 ? void 0 : initialData.name)
            ? { organizationId: initialData.orgId, name: initialData.name }
            : undefined,
    }), 2), stepFifthData = _o[0], setStepFifthData = _o[1];
    react_1.useEffect(function () {
        if (location.query.revalidateItunesSession && !revalidateItunesSession) {
            setIsLoading(true);
            setRevalidateItunesSession(location.query.revalidateItunesSession);
        }
    }, [location.query]);
    react_1.useEffect(function () {
        if (revalidateItunesSession) {
            handleStartItunesAuthentication(false);
            if (activeStep !== 3) {
                setActiveStep(3);
            }
            setIsLoading(false);
            return;
        }
        setIsLoading(false);
    }, [revalidateItunesSession]);
    function checkAppStoreConnectCredentials() {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var response, error_1;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        setIsLoading(true);
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + orgSlug + "/" + projectSlug + "/appstoreconnect/apps/", {
                                method: 'POST',
                                data: {
                                    appconnectIssuer: stepOneData.issuer,
                                    appconnectKey: stepOneData.keyId,
                                    appconnectPrivateKey: stepOneData.privateKey,
                                },
                            })];
                    case 2:
                        response = _a.sent();
                        setAppStoreApps(response.apps);
                        setStepTwoData({ app: response.apps[0] });
                        setIsLoading(false);
                        goNext();
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _a.sent();
                        setIsLoading(false);
                        indicator_1.addErrorMessage(locale_1.t('We could not establish a connection with App Store Connect. Please check the entered App Store Connect credentials.'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    }
    function startTwoFactorAuthentication(shouldJumpNext) {
        if (shouldJumpNext === void 0) { shouldJumpNext = false; }
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var response, organizations, newSessionContext, error_2;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        setIsLoading(true);
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + orgSlug + "/" + projectSlug + "/appstoreconnect/2fa/", {
                                method: 'POST',
                                data: {
                                    code: stepFourData.authenticationCode,
                                    useSms: useSms,
                                    sessionContext: sessionContext,
                                },
                            })];
                    case 2:
                        response = _a.sent();
                        organizations = response.organizations, newSessionContext = response.sessionContext;
                        if (shouldJumpNext) {
                            persistData(newSessionContext);
                            return [2 /*return*/];
                        }
                        setSessionContext(newSessionContext);
                        setAppleStoreOrgs(organizations);
                        setStepFifthData({ org: organizations[0] });
                        setIsLoading(false);
                        goNext();
                        return [3 /*break*/, 4];
                    case 3:
                        error_2 = _a.sent();
                        setIsLoading(false);
                        indicator_1.addErrorMessage(locale_1.t('The two factor authentication failed. Please check the entered code.'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    }
    function persistData(newSessionContext) {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var endpoint, errorMessage, response, error_3;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (!stepTwoData.app || !stepFifthData.org || !stepThreeData.username) {
                            return [2 /*return*/];
                        }
                        setIsLoading(true);
                        endpoint = "/projects/" + orgSlug + "/" + projectSlug + "/appstoreconnect/";
                        errorMessage = locale_1.t('An error occured while adding the App Store Connect repository.');
                        if (!!initialData) {
                            endpoint = "" + endpoint + initialData.id + "/";
                            errorMessage = locale_1.t('An error occured while updating the App Store Connect repository.');
                        }
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise(endpoint, {
                                method: 'POST',
                                data: {
                                    itunesUser: stepThreeData.username,
                                    itunesPassword: stepThreeData.password,
                                    appconnectIssuer: stepOneData.issuer,
                                    appconnectKey: stepOneData.keyId,
                                    appconnectPrivateKey: stepOneData.privateKey,
                                    appName: stepTwoData.app.name,
                                    appId: stepTwoData.app.appId,
                                    bundleId: stepTwoData.app.bundleId,
                                    orgId: stepFifthData.org.organizationId,
                                    orgName: stepFifthData.org.name,
                                    sessionContext: newSessionContext !== null && newSessionContext !== void 0 ? newSessionContext : sessionContext,
                                },
                            })];
                    case 2:
                        response = _a.sent();
                        onSubmit(response);
                        return [3 /*break*/, 4];
                    case 3:
                        error_3 = _a.sent();
                        setIsLoading(false);
                        indicator_1.addErrorMessage(errorMessage);
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    }
    function isFormInvalid() {
        switch (activeStep) {
            case 0:
                return Object.keys(stepOneData).some(function (key) { return !stepOneData[key]; });
            case 1:
                return Object.keys(stepTwoData).some(function (key) { return !stepTwoData[key]; });
            case 2: {
                return Object.keys(stepThreeData).some(function (key) { return !stepThreeData[key]; });
            }
            case 3: {
                return Object.keys(stepFourData).some(function (key) { return !stepFourData[key]; });
            }
            case 4: {
                return Object.keys(stepFifthData).some(function (key) { return !stepFifthData[key]; });
            }
            default:
                return false;
        }
    }
    function goNext() {
        setActiveStep(activeStep + 1);
    }
    function handleStartItunesAuthentication(shouldGoNext) {
        if (shouldGoNext === void 0) { shouldGoNext = true; }
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var response, _a;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        if (shouldGoNext) {
                            setIsLoading(true);
                        }
                        if (useSms) {
                            setUseSms(false);
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + orgSlug + "/" + projectSlug + "/appstoreconnect/start/", {
                                method: 'POST',
                                data: {
                                    itunesUser: stepThreeData.username,
                                    itunesPassword: stepThreeData.password,
                                },
                            })];
                    case 2:
                        response = _b.sent();
                        setSessionContext(response.sessionContext);
                        if (shouldGoNext) {
                            setIsLoading(false);
                            goNext();
                        }
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        if (shouldGoNext) {
                            setIsLoading(false);
                        }
                        indicator_1.addErrorMessage(locale_1.t('The iTunes authentication failed. Please check the entered credentials.'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    }
    function handleStartSmsAuthentication() {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var response, _a;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        if (!useSms) {
                            setUseSms(true);
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise("/projects/" + orgSlug + "/" + projectSlug + "/appstoreconnect/requestSms/", {
                                method: 'POST',
                                data: { sessionContext: sessionContext },
                            })];
                    case 2:
                        response = _b.sent();
                        setSessionContext(response.sessionContext);
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        indicator_1.addErrorMessage(locale_1.t('An error occured while sending the SMS. Please try again'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    }
    function handleGoBack() {
        var newActiveStep = activeStep - 1;
        switch (newActiveStep) {
            case 3:
                handleStartItunesAuthentication(false);
                setStepFourData({ authenticationCode: undefined });
                break;
            default:
                break;
        }
        setActiveStep(newActiveStep);
    }
    function handleGoNext() {
        switch (activeStep) {
            case 0:
                checkAppStoreConnectCredentials();
                break;
            case 1:
                goNext();
                break;
            case 2:
                handleStartItunesAuthentication();
                break;
            case 3:
                startTwoFactorAuthentication();
                break;
            case 4:
                persistData();
                break;
            default:
                break;
        }
    }
    function renderCurrentStep() {
        switch (activeStep) {
            case 0:
                return <stepOne_1.default stepOneData={stepOneData} onSetStepOneData={setStepOneData}/>;
            case 1:
                return (<stepTwo_1.default appStoreApps={appStoreApps} stepTwoData={stepTwoData} onSetStepTwoData={setStepTwoData}/>);
            case 2:
                return (<stepThree_1.default stepThreeData={stepThreeData} onSetStepOneData={setStepThreeData}/>);
            case 3:
                return (<stepFour_1.default stepFourData={stepFourData} onSetStepFourData={setStepFourData} onStartItunesAuthentication={handleStartItunesAuthentication} onStartSmsAuthentication={handleStartSmsAuthentication}/>);
            case 4:
                return (<stepFifth_1.default appleStoreOrgs={appleStoreOrgs} stepFifthData={stepFifthData} onSetStepFifthData={setStepFifthData}/>);
            default:
                return (<alert_1.default type="error" icon={<icons_1.IconWarning />}>
            {locale_1.t('This step could not be found.')}
          </alert_1.default>);
        }
    }
    function getAlerts() {
        var alerts = [];
        if (revalidateItunesSession) {
            if (!updateAlertMessage && revalidateItunesSession) {
                alerts.push(<StyledAlert type="warning" icon={<icons_1.IconWarning />}>
            {locale_1.t('Your iTunes session has already been re-validated.')}
          </StyledAlert>);
            }
            return alerts;
        }
        if (activeStep !== 0) {
            return alerts;
        }
        if (updateAlertMessage === utils_1.appStoreConnectAlertMessage.appStoreCredentialsInvalid) {
            alerts.push(<StyledAlert type="warning" icon={<icons_1.IconWarning />}>
          {locale_1.t('Your App Store Connect credentials are invalid. To reconnect, update your credentials.')}
        </StyledAlert>);
        }
        if (updateAlertMessage === utils_1.appStoreConnectAlertMessage.iTunesSessionInvalid) {
            alerts.push(<alertLink_1.default withoutMarginBottom icon={<icons_1.IconWarning />} to={{
                    pathname: location.pathname,
                    query: tslib_1.__assign(tslib_1.__assign({}, location.query), { revalidateItunesSession: true }),
                }}>
          {locale_1.t('Your iTunes session has expired. To reconnect, revalidate the session.')}
        </alertLink_1.default>);
        }
        if (updateAlertMessage ===
            utils_1.appStoreConnectAlertMessage.isTodayAfterItunesSessionRefreshAt) {
            alerts.push(<alertLink_1.default withoutMarginBottom icon={<icons_1.IconWarning />} to={{
                    pathname: location.pathname,
                    query: tslib_1.__assign(tslib_1.__assign({}, location.query), { revalidateItunesSession: true }),
                }}>
          {locale_1.t('Your iTunes session will likely expire soon. We recommend that you revalidate the session.')}
        </alertLink_1.default>);
        }
        return alerts;
    }
    function renderBodyContent() {
        var alerts = getAlerts();
        return (<react_1.Fragment>
        {!!alerts.length && (<Alerts marginBottom={activeStep === 3 ? 1.5 : 3}>
            {alerts.map(function (alert, index) { return (<react_1.Fragment key={index}>{alert}</react_1.Fragment>); })}
          </Alerts>)}
        {renderCurrentStep()}
      </react_1.Fragment>);
    }
    if (initialData && !appStoreConnectContext) {
        return <loadingIndicator_1.default />;
    }
    if (revalidateItunesSession) {
        return (<react_1.Fragment>
        <Header closeButton>
          <HeaderContentTitle>{locale_1.t('Revalidate iTunes session')}</HeaderContentTitle>
        </Header>
        <Body>{renderBodyContent()}</Body>
        <Footer>
          <StyledButton priority="primary" onClick={function () { return startTwoFactorAuthentication(true); }} disabled={isLoading || isFormInvalid()}>
            {locale_1.t('Revalidate')}
          </StyledButton>
        </Footer>
      </react_1.Fragment>);
    }
    return (<react_1.Fragment>
      <Header closeButton>
        <HeaderContent>
          <NumericSymbol>{activeStep + 1}</NumericSymbol>
          <HeaderContentTitle>{steps[activeStep]}</HeaderContentTitle>
          <StepsOverview>
            {locale_1.tct('[currentStep] of [totalSteps]', {
            currentStep: activeStep + 1,
            totalSteps: steps.length,
        })}
          </StepsOverview>
        </HeaderContent>
      </Header>
      <Body>{renderBodyContent()}</Body>
      <Footer>
        <buttonBar_1.default gap={1}>
          {activeStep !== 0 && <button_1.default onClick={handleGoBack}>{locale_1.t('Back')}</button_1.default>}
          <StyledButton priority="primary" onClick={handleGoNext} disabled={isLoading || isFormInvalid()}>
            {isLoading && (<LoadingIndicatorWrapper>
                <loadingIndicator_1.default mini/>
              </LoadingIndicatorWrapper>)}
            {activeStep + 1 === steps.length
            ? initialData
                ? locale_1.t('Update')
                : locale_1.t('Save')
            : steps[activeStep + 1]}
          </StyledButton>
        </buttonBar_1.default>
      </Footer>
    </react_1.Fragment>);
}
exports.default = withApi_1.default(AppStoreConnect);
var HeaderContent = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content max-content 1fr;\n  align-items: center;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: max-content max-content 1fr;\n  align-items: center;\n  grid-gap: ", ";\n"])), space_1.default(1));
var NumericSymbol = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  border-radius: 50%;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  width: 24px;\n  height: 24px;\n  font-weight: 700;\n  font-size: ", ";\n  background-color: ", ";\n"], ["\n  border-radius: 50%;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n  width: 24px;\n  height: 24px;\n  font-weight: 700;\n  font-size: ", ";\n  background-color: ", ";\n"])), function (p) { return p.theme.fontSizeMedium; }, function (p) { return p.theme.yellow300; });
var HeaderContentTitle = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-weight: 700;\n  font-size: ", ";\n"], ["\n  font-weight: 700;\n  font-size: ", ";\n"])), function (p) { return p.theme.fontSizeExtraLarge; });
var StepsOverview = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  display: flex;\n  justify-content: flex-end;\n"], ["\n  color: ", ";\n  display: flex;\n  justify-content: flex-end;\n"])), function (p) { return p.theme.gray300; });
var LoadingIndicatorWrapper = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  height: 100%;\n  position: absolute;\n  width: 100%;\n  top: 0;\n  left: 0;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"], ["\n  height: 100%;\n  position: absolute;\n  width: 100%;\n  top: 0;\n  left: 0;\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"])));
var StyledButton = styled_1.default(button_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  position: relative;\n"], ["\n  position: relative;\n"])));
var Alerts = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  margin-bottom: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  margin-bottom: ", ";\n"])), space_1.default(1.5), function (p) { return space_1.default(p.marginBottom); });
var StyledAlert = styled_1.default(alert_1.default)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8;
//# sourceMappingURL=index.jsx.map