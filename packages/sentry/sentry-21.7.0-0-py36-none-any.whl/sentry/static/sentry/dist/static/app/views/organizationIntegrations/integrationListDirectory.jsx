Object.defineProperty(exports, "__esModule", { value: true });
exports.IntegrationListDirectory = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var debounce_1 = tslib_1.__importDefault(require("lodash/debounce"));
var flatten_1 = tslib_1.__importDefault(require("lodash/flatten"));
var groupBy_1 = tslib_1.__importDefault(require("lodash/groupBy"));
var startCase_1 = tslib_1.__importDefault(require("lodash/startCase"));
var uniq_1 = tslib_1.__importDefault(require("lodash/uniq"));
var queryString = tslib_1.__importStar(require("query-string"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var selectControl_1 = tslib_1.__importDefault(require("app/components/forms/selectControl"));
var panels_1 = require("app/components/panels");
var searchBar_1 = tslib_1.__importDefault(require("app/components/searchBar"));
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var createFuzzySearch_1 = require("app/utils/createFuzzySearch");
var integrationUtil_1 = require("app/utils/integrationUtil");
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var permissionAlert_1 = tslib_1.__importDefault(require("app/views/settings/organization/permissionAlert"));
var constants_1 = require("./constants");
var integrationRow_1 = tslib_1.__importDefault(require("./integrationRow"));
var fuseOptions = {
    threshold: 0.3,
    location: 0,
    distance: 100,
    includeScore: true,
    keys: ['slug', 'key', 'name', 'id'],
};
var TEXT_SEARCH_ANALYTICS_DEBOUNCE_IN_MS = 1000;
var IntegrationListDirectory = /** @class */ (function (_super) {
    tslib_1.__extends(IntegrationListDirectory, _super);
    function IntegrationListDirectory() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        // Some integrations require visiting a different website to add them. When
        // we come back to the tab we want to show our integrations as soon as we can.
        _this.shouldReload = true;
        _this.reloadOnVisible = true;
        _this.shouldReloadOnVisible = true;
        _this.getAppInstall = function (app) { var _a; return (_a = _this.state.appInstalls) === null || _a === void 0 ? void 0 : _a.find(function (i) { return i.app.slug === app.slug; }); };
        _this.getPopularityWeight = function (integration) { var _a; return (_a = constants_1.POPULARITY_WEIGHT[integration.slug]) !== null && _a !== void 0 ? _a : 1; };
        _this.sortByName = function (a, b) {
            return a.slug.localeCompare(b.slug);
        };
        _this.sortByPopularity = function (a, b) {
            var weightA = _this.getPopularityWeight(a);
            var weightB = _this.getPopularityWeight(b);
            return weightB - weightA;
        };
        _this.sortByInstalled = function (a, b) {
            return _this.getInstallValue(b) - _this.getInstallValue(a);
        };
        _this.debouncedTrackIntegrationSearch = debounce_1.default(function (search, numResults) {
            integrationUtil_1.trackIntegrationEvent('integrations.directory_item_searched', {
                view: 'integrations_directory',
                search_term: search,
                num_results: numResults,
            }, _this.props.organization);
        }, TEXT_SEARCH_ANALYTICS_DEBOUNCE_IN_MS);
        /**
         * Get filter parameters and guard against `queryString.parse` returning arrays.
         */
        _this.getFilterParameters = function () {
            var _a = queryString.parse(_this.props.location.search), category = _a.category, search = _a.search;
            var selectedCategory = Array.isArray(category) ? category[0] : category || '';
            var searchInput = Array.isArray(search) ? search[0] : search || '';
            return { searchInput: searchInput, selectedCategory: selectedCategory };
        };
        /**
         * Update the query string with the current filter parameter values.
         */
        _this.updateQueryString = function () {
            var _a = _this.state, searchInput = _a.searchInput, selectedCategory = _a.selectedCategory;
            var searchString = queryString.stringify(tslib_1.__assign(tslib_1.__assign({}, queryString.parse(_this.props.location.search)), { search: searchInput ? searchInput : undefined, category: selectedCategory ? selectedCategory : undefined }));
            react_router_1.browserHistory.replace({
                pathname: _this.props.location.pathname,
                search: searchString ? "?" + searchString : undefined,
            });
        };
        /**
         * Filter the integrations list by ANDing together the search query and the category select.
         */
        _this.updateDisplayedList = function () {
            var _a = _this.state, fuzzy = _a.fuzzy, list = _a.list, searchInput = _a.searchInput, selectedCategory = _a.selectedCategory;
            var displayedList = list;
            if (searchInput && fuzzy) {
                var searchResults = fuzzy.search(searchInput);
                displayedList = _this.sortIntegrations(searchResults.map(function (i) { return i.item; }));
            }
            if (selectedCategory) {
                displayedList = displayedList.filter(function (integration) {
                    return integrationUtil_1.getCategoriesForIntegration(integration).includes(selectedCategory);
                });
            }
            _this.setState({ displayedList: displayedList });
            return displayedList;
        };
        _this.handleSearchChange = function (value) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _this = this;
            return tslib_1.__generator(this, function (_a) {
                this.setState({ searchInput: value }, function () {
                    _this.updateQueryString();
                    var result = _this.updateDisplayedList();
                    if (value) {
                        _this.debouncedTrackIntegrationSearch(value, result.length);
                    }
                });
                return [2 /*return*/];
            });
        }); };
        _this.onCategorySelect = function (_a) {
            var category = _a.value;
            _this.setState({ selectedCategory: category }, function () {
                _this.updateQueryString();
                _this.updateDisplayedList();
                if (category) {
                    integrationUtil_1.trackIntegrationEvent('integrations.directory_category_selected', {
                        view: 'integrations_directory',
                        category: category,
                    }, _this.props.organization);
                }
            });
        };
        // Rendering
        _this.renderProvider = function (provider) {
            var _a, _b;
            var organization = _this.props.organization;
            // find the integration installations for that provider
            var integrations = (_b = (_a = _this.state.integrations) === null || _a === void 0 ? void 0 : _a.filter(function (i) { return i.provider.key === provider.key; })) !== null && _b !== void 0 ? _b : [];
            return (<integrationRow_1.default key={"row-" + provider.key} data-test-id="integration-row" organization={organization} type="firstParty" slug={provider.slug} displayName={provider.name} status={integrations.length ? 'Installed' : 'Not Installed'} publishStatus="published" configurations={integrations.length} categories={integrationUtil_1.getCategoriesForIntegration(provider)}/>);
        };
        _this.renderPlugin = function (plugin) {
            var organization = _this.props.organization;
            var isLegacy = plugin.isHidden;
            var displayName = plugin.name + " " + (isLegacy ? '(Legacy)' : '');
            // hide legacy integrations if we don't have any projects with them
            if (isLegacy && !plugin.projectList.length) {
                return null;
            }
            return (<integrationRow_1.default key={"row-plugin-" + plugin.id} data-test-id="integration-row" organization={organization} type="plugin" slug={plugin.slug} displayName={displayName} status={plugin.projectList.length ? 'Installed' : 'Not Installed'} publishStatus="published" configurations={plugin.projectList.length} categories={integrationUtil_1.getCategoriesForIntegration(plugin)}/>);
        };
        // render either an internal or non-internal app
        _this.renderSentryApp = function (app) {
            var organization = _this.props.organization;
            var status = integrationUtil_1.getSentryAppInstallStatus(_this.getAppInstall(app));
            var categories = integrationUtil_1.getCategoriesForIntegration(app);
            return (<integrationRow_1.default key={"sentry-app-row-" + app.slug} data-test-id="integration-row" organization={organization} type="sentryApp" slug={app.slug} displayName={app.name} status={status} publishStatus={app.status} configurations={0} categories={categories}/>);
        };
        _this.renderDocumentIntegration = function (integration) {
            var organization = _this.props.organization;
            return (<integrationRow_1.default key={"doc-int-" + integration.slug} organization={organization} type="documentIntegration" slug={integration.slug} displayName={integration.name} publishStatus="published" configurations={0} categories={integrationUtil_1.getCategoriesForIntegration(integration)}/>);
        };
        _this.renderIntegration = function (integration) {
            if (integrationUtil_1.isSentryApp(integration)) {
                return _this.renderSentryApp(integration);
            }
            if (integrationUtil_1.isPlugin(integration)) {
                return _this.renderPlugin(integration);
            }
            if (integrationUtil_1.isDocumentIntegration(integration)) {
                return _this.renderDocumentIntegration(integration);
            }
            return _this.renderProvider(integration);
        };
        return _this;
    }
    IntegrationListDirectory.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { list: [], displayedList: [], selectedCategory: '' });
    };
    IntegrationListDirectory.prototype.onLoadAllEndpointsSuccess = function () {
        var _this = this;
        var _a = this.state, publishedApps = _a.publishedApps, orgOwnedApps = _a.orgOwnedApps, extraApp = _a.extraApp, plugins = _a.plugins;
        var published = publishedApps || [];
        // If we have an extra app in state from query parameter, add it as org owned app
        if (orgOwnedApps !== null && extraApp) {
            orgOwnedApps.push(extraApp);
        }
        // we dont want the app to render twice if its the org that created
        // the published app.
        var orgOwned = orgOwnedApps === null || orgOwnedApps === void 0 ? void 0 : orgOwnedApps.filter(function (app) { return !published.find(function (p) { return p.slug === app.slug; }); });
        /**
         * We should have three sections:
         * 1. Public apps and integrations available to everyone
         * 2. Unpublished apps available to that org
         * 3. Internal apps available to that org
         */
        var combined = []
            .concat(published)
            .concat(orgOwned !== null && orgOwned !== void 0 ? orgOwned : [])
            .concat(this.providers)
            .concat(plugins !== null && plugins !== void 0 ? plugins : [])
            .concat(Object.values(constants_1.documentIntegrations));
        var list = this.sortIntegrations(combined);
        var _b = this.getFilterParameters(), searchInput = _b.searchInput, selectedCategory = _b.selectedCategory;
        this.setState({ list: list, searchInput: searchInput, selectedCategory: selectedCategory }, function () {
            _this.updateDisplayedList();
            _this.trackPageViewed();
        });
    };
    IntegrationListDirectory.prototype.trackPageViewed = function () {
        // count the number of installed apps
        var _a = this.state, integrations = _a.integrations, publishedApps = _a.publishedApps, plugins = _a.plugins;
        var integrationsInstalled = new Set();
        // add installed integrations
        integrations === null || integrations === void 0 ? void 0 : integrations.forEach(function (integration) {
            integrationsInstalled.add(integration.provider.key);
        });
        // add sentry apps
        publishedApps === null || publishedApps === void 0 ? void 0 : publishedApps.filter(this.getAppInstall).forEach(function (sentryApp) {
            integrationsInstalled.add(sentryApp.slug);
        });
        // add plugins
        plugins === null || plugins === void 0 ? void 0 : plugins.forEach(function (plugin) {
            if (plugin.projectList.length) {
                integrationsInstalled.add(plugin.slug);
            }
        });
        integrationUtil_1.trackIntegrationEvent('integrations.index_viewed', {
            integrations_installed: integrationsInstalled.size,
            view: 'integrations_directory',
        }, this.props.organization, { startSession: true });
    };
    IntegrationListDirectory.prototype.getEndpoints = function () {
        var orgId = this.props.params.orgId;
        var baseEndpoints = [
            ['config', "/organizations/" + orgId + "/config/integrations/"],
            [
                'integrations',
                "/organizations/" + orgId + "/integrations/",
                { query: { includeConfig: 0 } },
            ],
            ['orgOwnedApps', "/organizations/" + orgId + "/sentry-apps/"],
            ['publishedApps', '/sentry-apps/', { query: { status: 'published' } }],
            ['appInstalls', "/organizations/" + orgId + "/sentry-app-installations/"],
            ['plugins', "/organizations/" + orgId + "/plugins/configs/"],
        ];
        /**
         * optional app to load for super users
         * should only be done for unpublished integrations from another org
         * but no checks are in place to ensure the above condition
         */
        var extraAppSlug = new URLSearchParams(this.props.location.search).get('extra_app');
        if (extraAppSlug) {
            baseEndpoints.push(['extraApp', "/sentry-apps/" + extraAppSlug + "/"]);
        }
        return baseEndpoints;
    };
    Object.defineProperty(IntegrationListDirectory.prototype, "unmigratableReposByOrg", {
        // State
        get: function () {
            // Group by [GitHub|BitBucket|VSTS] Org name
            return groupBy_1.default(this.state.unmigratableRepos, function (repo) { return repo.name.split('/')[0]; });
        },
        enumerable: false,
        configurable: true
    });
    Object.defineProperty(IntegrationListDirectory.prototype, "providers", {
        get: function () {
            var _a, _b;
            return (_b = (_a = this.state.config) === null || _a === void 0 ? void 0 : _a.providers) !== null && _b !== void 0 ? _b : [];
        },
        enumerable: false,
        configurable: true
    });
    // Returns 0 if uninstalled, 1 if pending, and 2 if installed
    IntegrationListDirectory.prototype.getInstallValue = function (integration) {
        var integrations = this.state.integrations;
        if (integrationUtil_1.isPlugin(integration)) {
            return integration.projectList.length > 0 ? 2 : 0;
        }
        if (integrationUtil_1.isSentryApp(integration)) {
            var install = this.getAppInstall(integration);
            if (install) {
                return install.status === 'pending' ? 1 : 2;
            }
            return 0;
        }
        if (integrationUtil_1.isDocumentIntegration(integration)) {
            return 0;
        }
        return (integrations === null || integrations === void 0 ? void 0 : integrations.find(function (i) { return i.provider.key === integration.key; })) ? 2 : 0;
    };
    IntegrationListDirectory.prototype.sortIntegrations = function (integrations) {
        var _this = this;
        return integrations.sort(function (a, b) {
            // sort by whether installed first
            var diffWeight = _this.sortByInstalled(a, b);
            if (diffWeight !== 0) {
                return diffWeight;
            }
            // then sort by popularity
            var diffPop = _this.sortByPopularity(a, b);
            if (diffPop !== 0) {
                return diffPop;
            }
            // then sort by name
            return _this.sortByName(a, b);
        });
    };
    IntegrationListDirectory.prototype.componentDidUpdate = function (_, prevState) {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        if (!(this.state.list.length !== prevState.list.length)) return [3 /*break*/, 2];
                        return [4 /*yield*/, this.createSearch()];
                    case 1:
                        _a.sent();
                        _a.label = 2;
                    case 2: return [2 /*return*/];
                }
            });
        });
    };
    IntegrationListDirectory.prototype.createSearch = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var list, _a;
            var _b;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        list = this.state.list;
                        _a = this.setState;
                        _b = {};
                        return [4 /*yield*/, createFuzzySearch_1.createFuzzySearch(list || [], fuseOptions)];
                    case 1:
                        _a.apply(this, [(_b.fuzzy = _c.sent(),
                                _b)]);
                        return [2 /*return*/];
                }
            });
        });
    };
    IntegrationListDirectory.prototype.renderBody = function () {
        var orgId = this.props.params.orgId;
        var _a = this.state, displayedList = _a.displayedList, list = _a.list, searchInput = _a.searchInput, selectedCategory = _a.selectedCategory;
        var title = locale_1.t('Integrations');
        var categoryList = uniq_1.default(flatten_1.default(list.map(integrationUtil_1.getCategoriesForIntegration))).sort();
        return (<react_1.Fragment>
        <sentryDocumentTitle_1.default title={title} orgSlug={orgId}/>

        {!this.props.hideHeader && (<settingsPageHeader_1.default title={title} action={<ActionContainer>
                <selectControl_1.default name="select-categories" onChange={this.onCategorySelect} value={selectedCategory} choices={tslib_1.__spreadArray([
                        ['', locale_1.t('All Categories')]
                    ], tslib_1.__read(categoryList.map(function (category) { return [category, startCase_1.default(category)]; })))}/>
                <searchBar_1.default query={searchInput || ''} onChange={this.handleSearchChange} placeholder={locale_1.t('Filter Integrations...')} width="25em"/>
              </ActionContainer>}/>)}

        <permissionAlert_1.default access={['org:integrations']}/>
        <panels_1.Panel>
          <panels_1.PanelBody>
            {displayedList.length ? (displayedList.map(this.renderIntegration)) : (<EmptyResultsContainer>
                <EmptyResultsBody>
                  {locale_1.tct('No Integrations found for "[searchTerm]".', {
                    searchTerm: searchInput,
                })}
                </EmptyResultsBody>
                <EmptyResultsBodyBold>
                  {locale_1.t("Not seeing what you're looking for?")}
                </EmptyResultsBodyBold>
                <EmptyResultsBody>
                  {locale_1.tct('[link:Build it on the Sentry Integration Platform.]', {
                    link: (<a href="https://docs.sentry.io/product/integrations/integration-platform/"/>),
                })}
                </EmptyResultsBody>
              </EmptyResultsContainer>)}
          </panels_1.PanelBody>
        </panels_1.Panel>
      </react_1.Fragment>);
    };
    return IntegrationListDirectory;
}(asyncComponent_1.default));
exports.IntegrationListDirectory = IntegrationListDirectory;
var ActionContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 240px max-content;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-template-columns: 240px max-content;\n  grid-gap: ", ";\n"])), space_1.default(2));
var EmptyResultsContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  height: 200px;\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  justify-content: center;\n"], ["\n  height: 200px;\n  display: flex;\n  flex-direction: column;\n  align-items: center;\n  justify-content: center;\n"])));
var EmptyResultsBody = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-size: 16px;\n  line-height: 28px;\n  color: ", ";\n  padding-bottom: ", ";\n"], ["\n  font-size: 16px;\n  line-height: 28px;\n  color: ", ";\n  padding-bottom: ", ";\n"])), function (p) { return p.theme.gray300; }, space_1.default(2));
var EmptyResultsBodyBold = styled_1.default(EmptyResultsBody)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  font-weight: bold;\n"], ["\n  font-weight: bold;\n"])));
exports.default = withOrganization_1.default(IntegrationListDirectory);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4;
//# sourceMappingURL=integrationListDirectory.jsx.map