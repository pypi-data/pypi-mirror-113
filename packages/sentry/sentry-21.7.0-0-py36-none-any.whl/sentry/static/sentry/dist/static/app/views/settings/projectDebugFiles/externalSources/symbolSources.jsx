Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var omit_1 = tslib_1.__importDefault(require("lodash/omit"));
var indicator_1 = require("app/actionCreators/indicator");
var modal_1 = require("app/actionCreators/modal");
var projectActions_1 = tslib_1.__importDefault(require("app/actions/projectActions"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var featureDisabled_1 = tslib_1.__importDefault(require("app/components/acl/featureDisabled"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var list_1 = tslib_1.__importDefault(require("app/components/list"));
var listItem_1 = tslib_1.__importDefault(require("app/components/list/listItem"));
var appStoreConnectContext_1 = tslib_1.__importDefault(require("app/components/projects/appStoreConnectContext"));
var utils_1 = require("app/components/projects/appStoreConnectContext/utils");
var textOverflow_1 = tslib_1.__importDefault(require("app/components/textOverflow"));
var debugFileSources_1 = require("app/data/debugFileSources");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_2 = require("app/utils");
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
var richListField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/richListField"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var utils_3 = require("./utils");
var dropDownItems = [
    {
        value: 's3',
        label: locale_1.t(debugFileSources_1.DEBUG_SOURCE_TYPES.s3),
        searchKey: locale_1.t('aws amazon s3 bucket'),
    },
    {
        value: 'gcs',
        label: locale_1.t(debugFileSources_1.DEBUG_SOURCE_TYPES.gcs),
        searchKey: locale_1.t('gcs google cloud storage bucket'),
    },
    {
        value: 'http',
        label: locale_1.t(debugFileSources_1.DEBUG_SOURCE_TYPES.http),
        searchKey: locale_1.t('http symbol server ssqp symstore symsrv'),
    },
];
function SymbolSources(_a) {
    var _b;
    var api = _a.api, organization = _a.organization, symbolSources = _a.symbolSources, projectSlug = _a.projectSlug, router = _a.router, location = _a.location;
    var appStoreConnectContext = react_1.useContext(appStoreConnectContext_1.default);
    react_1.useEffect(function () {
        openDebugFileSourceDialog();
    }, [location.query, appStoreConnectContext]);
    var hasAppConnectStoreFeatureFlag = !!((_b = organization.features) === null || _b === void 0 ? void 0 : _b.includes('app-store-connect'));
    if (hasAppConnectStoreFeatureFlag &&
        !appStoreConnectContext &&
        !dropDownItems.find(function (dropDownItem) { return dropDownItem.value === 'appStoreConnect'; })) {
        dropDownItems.push({
            value: 'appStoreConnect',
            label: locale_1.t(debugFileSources_1.DEBUG_SOURCE_TYPES.appStoreConnect),
            searchKey: locale_1.t('apple store connect itunes ios'),
        });
    }
    function getRichListFieldValue() {
        if (!hasAppConnectStoreFeatureFlag ||
            !appStoreConnectContext ||
            !appStoreConnectContext.updateAlertMessage) {
            return { value: symbolSources };
        }
        var symbolSourcesErrors = [];
        var symbolSourcesWarnings = [];
        var symbolSourcesWithErrors = symbolSources.map(function (symbolSource) {
            if (symbolSource.id === appStoreConnectContext.id) {
                var appStoreConnectErrors = [];
                var customRepositoryLink = "/settings/" + organization.slug + "/projects/" + projectSlug + "/debug-symbols/?customRepository=" + symbolSource.id;
                if (appStoreConnectContext.itunesSessionValid &&
                    appStoreConnectContext.appstoreCredentialsValid) {
                    var updateAlertMessage = appStoreConnectContext.updateAlertMessage;
                    if (updateAlertMessage ===
                        utils_1.appStoreConnectAlertMessage.isTodayAfterItunesSessionRefreshAt) {
                        symbolSourcesWarnings.push(<div>
                {locale_1.t('Your iTunes session will likely expire soon.')}
                &nbsp;
                {locale_1.tct('We recommend that you revalidate the session for [link]', {
                                link: (<link_1.default to={customRepositoryLink + "&revalidateItunesSession=true"}>
                      {symbolSource.name}
                    </link_1.default>),
                            })}
              </div>);
                        return tslib_1.__assign(tslib_1.__assign({}, symbolSource), { warning: updateAlertMessage });
                    }
                }
                if (appStoreConnectContext.itunesSessionValid === false) {
                    symbolSourcesErrors.push(locale_1.tct('Revalidate your iTunes session for [link]', {
                        link: (<link_1.default to={customRepositoryLink + "&revalidateItunesSession=true"}>
                  {symbolSource.name}
                </link_1.default>),
                    }));
                    appStoreConnectErrors.push(locale_1.t('Revalidate your iTunes session'));
                }
                if (appStoreConnectContext.appstoreCredentialsValid === false) {
                    symbolSourcesErrors.push(locale_1.tct('Recheck your App Store Credentials for [link]', {
                        link: <link_1.default to={customRepositoryLink}>{symbolSource.name}</link_1.default>,
                    }));
                    appStoreConnectErrors.push(locale_1.t('Recheck your App Store Credentials'));
                }
                return tslib_1.__assign(tslib_1.__assign({}, symbolSource), { error: !!appStoreConnectErrors.length ? (<react_1.Fragment>
              {locale_1.tn('There was an error connecting to the Apple Store Connect:', 'There were errors connecting to the Apple Store Connect:', appStoreConnectErrors.length)}
              <StyledList symbol="bullet">
                {appStoreConnectErrors.map(function (error, errorIndex) { return (<listItem_1.default key={errorIndex}>{error}</listItem_1.default>); })}
              </StyledList>
            </react_1.Fragment>) : undefined });
            }
            return symbolSource;
        });
        return {
            value: symbolSourcesWithErrors,
            errors: symbolSourcesErrors,
            warnings: symbolSourcesWarnings,
        };
    }
    var _c = getRichListFieldValue(), value = _c.value, _d = _c.warnings, warnings = _d === void 0 ? [] : _d, _e = _c.errors, errors = _e === void 0 ? [] : _e;
    function openDebugFileSourceDialog() {
        var customRepository = location.query.customRepository;
        if (!customRepository) {
            return;
        }
        var itemIndex = value.findIndex(function (v) { return v.id === customRepository; });
        var item = value[itemIndex];
        if (!item) {
            return;
        }
        var _warning = item._warning, _error = item._error, sourceConfig = tslib_1.__rest(item, ["_warning", "_error"]);
        modal_1.openDebugFileSourceModal({
            sourceConfig: sourceConfig,
            sourceType: item.type,
            appStoreConnectContext: appStoreConnectContext,
            onSave: function (updatedItem) {
                return handleSaveModal({ updatedItem: updatedItem, index: itemIndex });
            },
            onClose: handleCloseModal,
        });
    }
    function getRequestMessages(updatedSymbolSourcesQuantity) {
        if (updatedSymbolSourcesQuantity > symbolSources.length) {
            return {
                successMessage: locale_1.t('Successfully added custom repository'),
                errorMessage: locale_1.t('An error occurred while adding a new custom repository'),
            };
        }
        if (updatedSymbolSourcesQuantity < symbolSources.length) {
            return {
                successMessage: locale_1.t('Successfully removed custom repository'),
                errorMessage: locale_1.t('An error occurred while removing the custom repository'),
            };
        }
        return {
            successMessage: locale_1.t('Successfully updated custom repository'),
            errorMessage: locale_1.t('An error occurred while updating the custom repository'),
        };
    }
    function handleSaveModal(_a) {
        var updatedItems = _a.updatedItems, updatedItem = _a.updatedItem, index = _a.index;
        var items = updatedItems !== null && updatedItems !== void 0 ? updatedItems : [];
        if (updatedItem && utils_2.defined(index)) {
            items = tslib_1.__spreadArray([], tslib_1.__read(symbolSources));
            items.splice(index, 1, updatedItem);
        }
        var symbolSourcesWithoutErrors = items.map(function (item) {
            return omit_1.default(item, ['error', 'warning']);
        });
        var _b = getRequestMessages(items.length), successMessage = _b.successMessage, errorMessage = _b.errorMessage;
        var expandedSymbolSourceKeys = symbolSourcesWithoutErrors.map(utils_3.expandKeys);
        var promise = api.requestPromise("/projects/" + organization.slug + "/" + projectSlug + "/", {
            method: 'PUT',
            data: {
                symbolSources: JSON.stringify(expandedSymbolSourceKeys),
            },
        });
        promise.catch(function () {
            indicator_1.addErrorMessage(errorMessage);
        });
        promise.then(function (result) {
            projectActions_1.default.updateSuccess(result);
            indicator_1.addSuccessMessage(successMessage);
        });
        return promise;
    }
    function handleEditModal(repositoryId) {
        router.push(tslib_1.__assign(tslib_1.__assign({}, location), { query: tslib_1.__assign(tslib_1.__assign({}, location.query), { customRepository: repositoryId }) }));
    }
    function handleCloseModal() {
        router.push(tslib_1.__assign(tslib_1.__assign({}, location), { query: tslib_1.__assign(tslib_1.__assign({}, location.query), { customRepository: undefined, revalidateItunesSession: undefined }) }));
    }
    return (<react_1.Fragment>
      {!!warnings.length && (<alert_1.default type="warning" icon={<icons_1.IconRefresh />} system>
          {locale_1.tn('Please check the warning related to the following custom repository:', 'Please check the warnings related to the following custom repositories:', warnings.length)}
          <StyledList symbol="bullet">
            {warnings.map(function (warning, index) { return (<listItem_1.default key={index}>{warning}</listItem_1.default>); })}
          </StyledList>
        </alert_1.default>)}
      {!!errors.length && (<alert_1.default type="error" icon={<icons_1.IconWarning />} system>
          {locale_1.tn('There was an error connecting to the following custom repository:', 'There were errors connecting to the following custom repositories:', errors.length)}
          <StyledList symbol="bullet">
            {errors.map(function (error, index) { return (<listItem_1.default key={index}>{error}</listItem_1.default>); })}
          </StyledList>
        </alert_1.default>)}
      <field_1.default label={locale_1.t('Custom Repositories')} help={<feature_1.default features={['organizations:custom-symbol-sources']} hookName="feature-disabled:custom-symbol-sources" organization={organization} renderDisabled={function (p) { return (<featureDisabled_1.default features={p.features} message={locale_1.t('Custom repositories are disabled.')} featureName={locale_1.t('custom repositories')}/>); }}>
            {locale_1.t('Configures custom repositories containing debug files.')}
          </feature_1.default>} flexibleControlStateSize>
        <StyledRichListField inline={false} addButtonText={locale_1.t('Add Repository')} name="symbolSources" value={value} onChange={function (updatedItems) {
            handleSaveModal({ updatedItems: updatedItems });
        }} renderItem={function (item) {
            var _a;
            return (<textOverflow_1.default>{(_a = item.name) !== null && _a !== void 0 ? _a : locale_1.t('<Unnamed Repository>')}</textOverflow_1.default>);
        }} disabled={!organization.features.includes('custom-symbol-sources')} formatMessageValue={false} onEditItem={function (item) { return handleEditModal(item.id); }} onAddItem={function (item, addItem) {
            modal_1.openDebugFileSourceModal({
                sourceType: item.value,
                onSave: function (updatedData) { return Promise.resolve(addItem(updatedData)); },
            });
        }} removeConfirm={{
            onConfirm: function (item) {
                if (item.type === 'appStoreConnect') {
                    window.location.reload();
                }
            },
            confirmText: locale_1.t('Remove Repository'),
            message: (<react_1.Fragment>
                <textBlock_1.default>
                  <strong>
                    {locale_1.t('Removing this repository applies instantly to new events.')}
                  </strong>
                </textBlock_1.default>
                <textBlock_1.default>
                  {locale_1.t('Debug files from this repository will not be used to symbolicate future events. This may create new issues and alert members in your organization.')}
                </textBlock_1.default>
              </react_1.Fragment>),
        }} addDropdown={{ items: dropDownItems }}/>
      </field_1.default>
    </react_1.Fragment>);
}
exports.default = SymbolSources;
var StyledRichListField = styled_1.default(richListField_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var StyledList = styled_1.default(list_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space_1.default(1));
var templateObject_1, templateObject_2;
//# sourceMappingURL=symbolSources.jsx.map