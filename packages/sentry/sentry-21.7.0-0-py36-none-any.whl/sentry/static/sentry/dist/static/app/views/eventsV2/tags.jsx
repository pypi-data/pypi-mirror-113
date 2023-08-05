Object.defineProperty(exports, "__esModule", { value: true });
exports.Tags = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var events_1 = require("app/actionCreators/events");
var errorPanel_1 = tslib_1.__importDefault(require("app/components/charts/errorPanel"));
var styles_1 = require("app/components/charts/styles");
var emptyStateWarning_1 = tslib_1.__importDefault(require("app/components/emptyStateWarning"));
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var tagDistributionMeter_1 = tslib_1.__importDefault(require("app/components/tagDistributionMeter"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var eventView_1 = require("app/utils/discover/eventView");
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var Tags = /** @class */ (function (_super) {
    tslib_1.__extends(Tags, _super);
    function Tags() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            tags: [],
            totalValues: null,
            error: '',
        };
        _this.shouldRefetchData = function (prevProps) {
            var thisAPIPayload = _this.props.eventView.getFacetsAPIPayload(_this.props.location);
            var otherAPIPayload = prevProps.eventView.getFacetsAPIPayload(prevProps.location);
            return !eventView_1.isAPIPayloadSimilar(thisAPIPayload, otherAPIPayload);
        };
        _this.fetchData = function (forceFetchData) {
            if (forceFetchData === void 0) { forceFetchData = false; }
            return tslib_1.__awaiter(_this, void 0, void 0, function () {
                var _a, api, organization, eventView, location, confirmedQuery, tags, err_1;
                return tslib_1.__generator(this, function (_b) {
                    switch (_b.label) {
                        case 0:
                            _a = this.props, api = _a.api, organization = _a.organization, eventView = _a.eventView, location = _a.location, confirmedQuery = _a.confirmedQuery;
                            this.setState({ loading: true, error: '', tags: [] });
                            // Fetch should be forced after mounting as confirmedQuery isn't guaranteed
                            // since this component can mount/unmount via show/hide tags separate from
                            // data being loaded for the rest of the page.
                            if (!forceFetchData && confirmedQuery === false) {
                                return [2 /*return*/];
                            }
                            _b.label = 1;
                        case 1:
                            _b.trys.push([1, 3, , 4]);
                            return [4 /*yield*/, events_1.fetchTagFacets(api, organization.slug, eventView.getFacetsAPIPayload(location))];
                        case 2:
                            tags = _b.sent();
                            this.setState({ loading: false, tags: tags });
                            return [3 /*break*/, 4];
                        case 3:
                            err_1 = _b.sent();
                            Sentry.captureException(err_1);
                            this.setState({ loading: false, error: err_1 });
                            return [3 /*break*/, 4];
                        case 4: return [2 /*return*/];
                    }
                });
            });
        };
        _this.handleTagClick = function (tag) {
            var organization = _this.props.organization;
            // metrics
            analytics_1.trackAnalyticsEvent({
                eventKey: 'discover_v2.facet_map.clicked',
                eventName: 'Discoverv2: Clicked on a tag on the facet map',
                tag: tag,
                organization_id: parseInt(organization.id, 10),
            });
        };
        _this.renderBody = function () {
            var _a = _this.state, loading = _a.loading, error = _a.error, tags = _a.tags;
            if (loading) {
                return _this.renderPlaceholders();
            }
            if (error) {
                return (<errorPanel_1.default height="132px">
          <icons_1.IconWarning color="gray300" size="lg"/>
        </errorPanel_1.default>);
            }
            if (tags.length > 0) {
                return tags.map(function (tag) { return _this.renderTag(tag); });
            }
            else {
                return (<StyledEmptyStateWarning small>{locale_1.t('No tags found')}</StyledEmptyStateWarning>);
            }
        };
        return _this;
    }
    Tags.prototype.componentDidMount = function () {
        this.fetchData(true);
    };
    Tags.prototype.componentDidUpdate = function (prevProps) {
        if (this.shouldRefetchData(prevProps) ||
            prevProps.confirmedQuery !== this.props.confirmedQuery) {
            this.fetchData();
        }
    };
    Tags.prototype.renderTag = function (tag) {
        var _a = this.props, generateUrl = _a.generateUrl, totalValues = _a.totalValues;
        var segments = tag.topValues.map(function (segment) {
            segment.url = generateUrl(tag.key, segment.value);
            return segment;
        });
        // Ensure we don't show >100% if there's a slight mismatch between the facets
        // endpoint and the totals endpoint
        var maxTotalValues = segments.length > 0
            ? Math.max(Number(totalValues), segments[0].count)
            : totalValues;
        return (<tagDistributionMeter_1.default key={tag.key} title={tag.key} segments={segments} totalValues={Number(maxTotalValues)} renderLoading={function () { return <StyledPlaceholder height="16px"/>; }} onTagClick={this.handleTagClick} showReleasePackage/>);
    };
    Tags.prototype.renderPlaceholders = function () {
        return (<react_1.Fragment>
        <StyledPlaceholderTitle key="title-1"/>
        <StyledPlaceholder key="bar-1"/>
        <StyledPlaceholderTitle key="title-2"/>
        <StyledPlaceholder key="bar-2"/>
        <StyledPlaceholderTitle key="title-3"/>
        <StyledPlaceholder key="bar-3"/>
      </react_1.Fragment>);
    };
    Tags.prototype.render = function () {
        return (<react_1.Fragment>
        <styles_1.SectionHeading>{locale_1.t('Tag Summary')}</styles_1.SectionHeading>
        {this.renderBody()}
      </react_1.Fragment>);
    };
    return Tags;
}(react_1.Component));
exports.Tags = Tags;
var StyledEmptyStateWarning = styled_1.default(emptyStateWarning_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  height: 132px;\n  padding: 54px 15%;\n"], ["\n  height: 132px;\n  padding: 54px 15%;\n"])));
var StyledPlaceholder = styled_1.default(placeholder_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  border-radius: ", ";\n  height: 16px;\n  margin-bottom: ", ";\n"], ["\n  border-radius: ", ";\n  height: 16px;\n  margin-bottom: ", ";\n"])), function (p) { return p.theme.borderRadius; }, space_1.default(1.5));
var StyledPlaceholderTitle = styled_1.default(placeholder_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  width: 100px;\n  height: 12px;\n  margin-bottom: ", ";\n"], ["\n  width: 100px;\n  height: 12px;\n  margin-bottom: ", ";\n"])), space_1.default(0.5));
exports.default = withApi_1.default(Tags);
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=tags.jsx.map