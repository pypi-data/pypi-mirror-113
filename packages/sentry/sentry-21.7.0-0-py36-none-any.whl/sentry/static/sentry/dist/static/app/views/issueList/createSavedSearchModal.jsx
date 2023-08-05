Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var indicator_1 = require("app/actionCreators/indicator");
var savedSearches_1 = require("app/actionCreators/savedSearches");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var forms_1 = require("app/components/forms");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var utils_1 = require("./utils");
var DEFAULT_SORT_OPTIONS = [
    utils_1.IssueSortOptions.DATE,
    utils_1.IssueSortOptions.NEW,
    utils_1.IssueSortOptions.FREQ,
    utils_1.IssueSortOptions.PRIORITY,
    utils_1.IssueSortOptions.USER,
];
var CreateSavedSearchModal = /** @class */ (function (_super) {
    tslib_1.__extends(CreateSavedSearchModal, _super);
    function CreateSavedSearchModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            isSaving: false,
            name: '',
            error: null,
            query: null,
            sort: null,
        };
        _this.onSubmit = function (e) {
            var _a = _this.props, api = _a.api, organization = _a.organization;
            var query = _this.state.query || _this.props.query;
            var sort = _this.validateSortOption(_this.state.sort || _this.props.sort);
            e.preventDefault();
            _this.setState({ isSaving: true });
            indicator_1.addLoadingMessage(locale_1.t('Saving Changes'));
            savedSearches_1.createSavedSearch(api, organization.slug, _this.state.name, query, sort)
                .then(function (_data) {
                _this.props.closeModal();
                _this.setState({
                    error: null,
                    isSaving: false,
                });
                indicator_1.clearIndicators();
            })
                .catch(function (err) {
                var error = locale_1.t('Unable to save your changes.');
                if (err.responseJSON && err.responseJSON.detail) {
                    error = err.responseJSON.detail;
                }
                _this.setState({
                    error: error,
                    isSaving: false,
                });
                indicator_1.clearIndicators();
            });
        };
        _this.handleChangeName = function (val) {
            _this.setState({ name: String(val) });
        };
        _this.handleChangeQuery = function (val) {
            _this.setState({ query: String(val) });
        };
        _this.handleChangeSort = function (val) {
            _this.setState({ sort: val });
        };
        return _this;
    }
    /** Handle "date added" sort not being available for saved searches */
    CreateSavedSearchModal.prototype.validateSortOption = function (sort) {
        if (this.sortOptions().find(function (option) { return option === sort; })) {
            return sort;
        }
        return utils_1.IssueSortOptions.DATE;
    };
    CreateSavedSearchModal.prototype.sortOptions = function () {
        var _a;
        var organization = this.props.organization;
        var options = tslib_1.__spreadArray([], tslib_1.__read(DEFAULT_SORT_OPTIONS));
        if ((_a = organization === null || organization === void 0 ? void 0 : organization.features) === null || _a === void 0 ? void 0 : _a.includes('issue-list-trend-sort')) {
            options.push(utils_1.IssueSortOptions.TREND);
        }
        return options;
    };
    CreateSavedSearchModal.prototype.render = function () {
        var _a = this.state, isSaving = _a.isSaving, error = _a.error;
        var _b = this.props, Header = _b.Header, Footer = _b.Footer, Body = _b.Body, closeModal = _b.closeModal, query = _b.query, sort = _b.sort;
        var sortOptions = this.sortOptions().map(function (sortOption) { return ({
            value: sortOption,
            label: utils_1.getSortLabel(sortOption),
        }); });
        return (<form onSubmit={this.onSubmit}>
        <Header>
          <h4>{locale_1.t('Save Current Search')}</h4>
        </Header>

        <Body>
          {this.state.error && (<div className="alert alert-error alert-block">{error}</div>)}

          <p>{locale_1.t('All team members will now have access to this search.')}</p>
          <forms_1.TextField key="name" name="name" label={locale_1.t('Name')} placeholder="e.g. My Search Results" required onChange={this.handleChangeName}/>
          <forms_1.TextField key="query" name="query" label={locale_1.t('Query')} value={query} required onChange={this.handleChangeQuery}/>
          <forms_1.SelectField key="sort" name="sort" label={locale_1.t('Sort By')} required clearable={false} defaultValue={this.validateSortOption(sort)} options={sortOptions} onChange={this.handleChangeSort}/>
        </Body>
        <Footer>
          <button_1.default priority="default" size="small" disabled={isSaving} onClick={closeModal} style={{ marginRight: space_1.default(1) }}>
            {locale_1.t('Cancel')}
          </button_1.default>
          <button_1.default priority="primary" size="small" disabled={isSaving}>
            {locale_1.t('Save')}
          </button_1.default>
        </Footer>
      </form>);
    };
    return CreateSavedSearchModal;
}(React.Component));
exports.default = withApi_1.default(CreateSavedSearchModal);
//# sourceMappingURL=createSavedSearchModal.jsx.map