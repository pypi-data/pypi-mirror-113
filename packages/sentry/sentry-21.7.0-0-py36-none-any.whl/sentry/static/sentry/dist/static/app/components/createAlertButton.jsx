Object.defineProperty(exports, "__esModule", { value: true });
exports.CreateAlertFromViewButton = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var navigation_1 = require("app/actionCreators/navigation");
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var fields_1 = require("app/utils/discover/fields");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var constants_1 = require("app/views/alerts/incidentRules/constants");
var utils_1 = require("app/views/alerts/utils");
/**
 * Displays messages to the user on what needs to change in their query
 */
function IncompatibleQueryAlert(_a) {
    var incompatibleQuery = _a.incompatibleQuery, eventView = _a.eventView, orgId = _a.orgId, onClose = _a.onClose;
    var hasProjectError = incompatibleQuery.hasProjectError, hasEnvironmentError = incompatibleQuery.hasEnvironmentError, hasEventTypeError = incompatibleQuery.hasEventTypeError, hasYAxisError = incompatibleQuery.hasYAxisError;
    var totalErrors = Object.values(incompatibleQuery).filter(function (val) { return val === true; }).length;
    var eventTypeError = eventView.clone();
    eventTypeError.query += ' event.type:error';
    var eventTypeTransaction = eventView.clone();
    eventTypeTransaction.query += ' event.type:transaction';
    var eventTypeDefault = eventView.clone();
    eventTypeDefault.query += ' event.type:default';
    var eventTypeErrorDefault = eventView.clone();
    eventTypeErrorDefault.query += ' event.type:error or event.type:default';
    var pathname = "/organizations/" + orgId + "/discover/results/";
    var eventTypeLinks = {
        error: (<link_1.default to={{
                pathname: pathname,
                query: eventTypeError.generateQueryStringObject(),
            }}/>),
        default: (<link_1.default to={{
                pathname: pathname,
                query: eventTypeDefault.generateQueryStringObject(),
            }}/>),
        transaction: (<link_1.default to={{
                pathname: pathname,
                query: eventTypeTransaction.generateQueryStringObject(),
            }}/>),
        errorDefault: (<link_1.default to={{
                pathname: pathname,
                query: eventTypeErrorDefault.generateQueryStringObject(),
            }}/>),
    };
    return (<StyledAlert type="warning" icon={<icons_1.IconInfo color="yellow300" size="sm"/>}>
      {totalErrors === 1 && (<React.Fragment>
          {hasProjectError &&
                locale_1.t('An alert can use data from only one Project. Select one and try again.')}
          {hasEnvironmentError &&
                locale_1.t('An alert supports data from a single Environment or All Environments. Pick one try again.')}
          {hasEventTypeError &&
                locale_1.tct('An alert needs a filter of [error:event.type:error], [default:event.type:default], [transaction:event.type:transaction], [errorDefault:(event.type:error OR event.type:default)]. Use one of these and try again.', eventTypeLinks)}
          {hasYAxisError &&
                locale_1.tct('An alert can’t use the metric [yAxis] just yet. Select another metric and try again.', {
                    yAxis: <StyledCode>{eventView.getYAxis()}</StyledCode>,
                })}
        </React.Fragment>)}
      {totalErrors > 1 && (<React.Fragment>
          {locale_1.t('Yikes! That button didn’t work. Please fix the following problems:')}
          <StyledUnorderedList>
            {hasProjectError && <li>{locale_1.t('Select one Project.')}</li>}
            {hasEnvironmentError && (<li>{locale_1.t('Select a single Environment or All Environments.')}</li>)}
            {hasEventTypeError && (<li>
                {locale_1.tct('Use the filter [error:event.type:error], [default:event.type:default], [transaction:event.type:transaction], [errorDefault:(event.type:error OR event.type:default)].', eventTypeLinks)}
              </li>)}
            {hasYAxisError && (<li>
                {locale_1.tct('An alert can’t use the metric [yAxis] just yet. Select another metric and try again.', {
                    yAxis: <StyledCode>{eventView.getYAxis()}</StyledCode>,
                })}
              </li>)}
          </StyledUnorderedList>
        </React.Fragment>)}
      <StyledCloseButton icon={<icons_1.IconClose color="yellow300" size="sm" isCircled/>} aria-label={locale_1.t('Close')} size="zero" onClick={onClose} borderless/>
    </StyledAlert>);
}
function incompatibleYAxis(eventView) {
    var _a;
    var column = fields_1.explodeFieldString(eventView.getYAxis());
    if (column.kind === 'field' || column.kind === 'equation') {
        return true;
    }
    var eventTypeMatch = eventView.query.match(/event\.type:(transaction|error)/);
    if (!eventTypeMatch) {
        return false;
    }
    var dataset = eventTypeMatch[1];
    var yAxisConfig = dataset === 'error' ? constants_1.errorFieldConfig : constants_1.transactionFieldConfig;
    var invalidFunction = !yAxisConfig.aggregations.includes(column.function[0]);
    // Allow empty parameters, allow all numeric parameters - eg. apdex(300)
    var aggregation = fields_1.AGGREGATIONS[column.function[0]];
    if (!aggregation) {
        return false;
    }
    var isNumericParameter = aggregation.parameters.some(function (param) { return param.kind === 'value' && param.dataType === 'number'; });
    // There are other measurements possible, but for the time being, only allow alerting
    // on the predefined set of measurements for alerts.
    var allowedParameters = tslib_1.__spreadArray(tslib_1.__spreadArray([
        ''
    ], tslib_1.__read(yAxisConfig.fields)), tslib_1.__read(((_a = yAxisConfig.measurementKeys) !== null && _a !== void 0 ? _a : [])));
    var invalidParameter = !isNumericParameter && !allowedParameters.includes(column.function[1]);
    return invalidFunction || invalidParameter;
}
/**
 * Provide a button that can create an alert from an event view.
 * Emits incompatible query issues on click
 */
function CreateAlertFromViewButton(_a) {
    var projects = _a.projects, eventView = _a.eventView, organization = _a.organization, referrer = _a.referrer, onIncompatibleQuery = _a.onIncompatibleQuery, onSuccess = _a.onSuccess, buttonProps = tslib_1.__rest(_a, ["projects", "eventView", "organization", "referrer", "onIncompatibleQuery", "onSuccess"]);
    // Must have exactly one project selected and not -1 (all projects)
    var hasProjectError = eventView.project.length !== 1 || eventView.project[0] === -1;
    // Must have one or zero environments
    var hasEnvironmentError = eventView.environment.length > 1;
    // Must have event.type of error or transaction
    var hasEventTypeError = utils_1.getQueryDatasource(eventView.query) === null;
    // yAxis must be a function and enabled on alerts
    var hasYAxisError = incompatibleYAxis(eventView);
    var errors = {
        hasProjectError: hasProjectError,
        hasEnvironmentError: hasEnvironmentError,
        hasEventTypeError: hasEventTypeError,
        hasYAxisError: hasYAxisError,
    };
    var project = projects.find(function (p) { return p.id === "" + eventView.project[0]; });
    var hasErrors = Object.values(errors).some(function (x) { return x; });
    var to = hasErrors
        ? undefined
        : {
            pathname: "/organizations/" + organization.slug + "/alerts/" + (project === null || project === void 0 ? void 0 : project.slug) + "/new/",
            query: tslib_1.__assign(tslib_1.__assign({}, eventView.generateQueryStringObject()), { createFromDiscover: true, referrer: referrer }),
        };
    var handleClick = function (event) {
        if (hasErrors) {
            event.preventDefault();
            onIncompatibleQuery(function (onAlertClose) { return (<IncompatibleQueryAlert incompatibleQuery={errors} eventView={eventView} orgId={organization.slug} onClose={onAlertClose}/>); }, errors);
            return;
        }
        onSuccess();
    };
    return (<CreateAlertButton organization={organization} onClick={handleClick} to={to} {...buttonProps}/>);
}
exports.CreateAlertFromViewButton = CreateAlertFromViewButton;
var CreateAlertButton = withApi_1.default(react_router_1.withRouter(function (_a) {
    var organization = _a.organization, projectSlug = _a.projectSlug, iconProps = _a.iconProps, referrer = _a.referrer, router = _a.router, hideIcon = _a.hideIcon, api = _a.api, showPermissionGuide = _a.showPermissionGuide, buttonProps = tslib_1.__rest(_a, ["organization", "projectSlug", "iconProps", "referrer", "router", "hideIcon", "api", "showPermissionGuide"]);
    var createAlertUrl = function (providedProj) {
        var alertsBaseUrl = "/organizations/" + organization.slug + "/alerts/" + providedProj;
        return alertsBaseUrl + "/wizard/" + (referrer ? "?referrer=" + referrer : '');
    };
    function handleClickWithoutProject(event) {
        event.preventDefault();
        navigation_1.navigateTo(createAlertUrl(':projectId'), router);
    }
    function enableAlertsMemberWrite() {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var settingsEndpoint, err_1;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        settingsEndpoint = "/organizations/" + organization.slug + "/";
                        indicator_1.addLoadingMessage();
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise(settingsEndpoint, {
                                method: 'PUT',
                                data: {
                                    alertsMemberWrite: true,
                                },
                            })];
                    case 2:
                        _a.sent();
                        indicator_1.addSuccessMessage(locale_1.t('Successfully updated organization settings'));
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _a.sent();
                        indicator_1.addErrorMessage(locale_1.t('Unable to update organization settings'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    }
    var permissionTooltipText = locale_1.tct('Ask your organization owner or manager to [settingsLink:enable alerts access] for you.', { settingsLink: <link_1.default to={"/settings/" + organization.slug}/> });
    var renderButton = function (hasAccess) {
        var _a;
        return (<button_1.default disabled={!hasAccess} title={!hasAccess ? permissionTooltipText : undefined} icon={!hideIcon && <icons_1.IconSiren {...iconProps}/>} to={projectSlug ? createAlertUrl(projectSlug) : undefined} tooltipProps={{
                isHoverable: true,
                position: 'top',
                popperStyle: {
                    maxWidth: '270px',
                },
            }} onClick={projectSlug ? undefined : handleClickWithoutProject} {...buttonProps}>
          {(_a = buttonProps.children) !== null && _a !== void 0 ? _a : locale_1.t('Create Alert')}
        </button_1.default>);
    };
    var showGuide = !organization.alertsMemberWrite && !!showPermissionGuide;
    return (<access_1.default organization={organization} access={['alerts:write']}>
          {function (_a) {
            var hasAccess = _a.hasAccess;
            return showGuide ? (<access_1.default organization={organization} access={['org:write']}>
                {function (_a) {
                    var isOrgAdmin = _a.hasAccess;
                    return (<guideAnchor_1.default target={isOrgAdmin ? 'alerts_write_owner' : 'alerts_write_member'} onFinish={isOrgAdmin ? enableAlertsMemberWrite : undefined}>
                    {renderButton(hasAccess)}
                  </guideAnchor_1.default>);
                }}
              </access_1.default>) : (renderButton(hasAccess));
        }}
        </access_1.default>);
}));
exports.default = CreateAlertButton;
var StyledAlert = styled_1.default(alert_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  color: ", ";\n  margin-bottom: 0;\n"], ["\n  color: ", ";\n  margin-bottom: 0;\n"])), function (p) { return p.theme.textColor; });
var StyledUnorderedList = styled_1.default('ul')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-bottom: 0;\n"], ["\n  margin-bottom: 0;\n"])));
var StyledCode = styled_1.default('code')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  background-color: transparent;\n  padding: 0;\n"], ["\n  background-color: transparent;\n  padding: 0;\n"])));
var StyledCloseButton = styled_1.default(button_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  transition: opacity 0.1s linear;\n  position: absolute;\n  top: 3px;\n  right: 0;\n\n  &:hover,\n  &:focus {\n    background-color: transparent;\n    opacity: 1;\n  }\n"], ["\n  transition: opacity 0.1s linear;\n  position: absolute;\n  top: 3px;\n  right: 0;\n\n  &:hover,\n  &:focus {\n    background-color: transparent;\n    opacity: 1;\n  }\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=createAlertButton.jsx.map