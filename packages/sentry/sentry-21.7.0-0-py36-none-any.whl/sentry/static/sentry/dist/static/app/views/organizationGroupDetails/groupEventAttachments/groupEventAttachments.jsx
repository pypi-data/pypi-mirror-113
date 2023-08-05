Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var ReactRouter = tslib_1.__importStar(require("react-router"));
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var emptyStateWarning_1 = tslib_1.__importDefault(require("app/components/emptyStateWarning"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var groupEventAttachmentsFilter_1 = tslib_1.__importDefault(require("./groupEventAttachmentsFilter"));
var groupEventAttachmentsTable_1 = tslib_1.__importDefault(require("./groupEventAttachmentsTable"));
var GroupEventAttachments = /** @class */ (function (_super) {
    tslib_1.__extends(GroupEventAttachments, _super);
    function GroupEventAttachments() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function (deletedAttachmentId) {
            _this.setState(function (prevState) { return ({
                deletedAttachments: tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(prevState.deletedAttachments)), [deletedAttachmentId]),
            }); });
        };
        return _this;
    }
    GroupEventAttachments.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { deletedAttachments: [] });
    };
    GroupEventAttachments.prototype.getEndpoints = function () {
        var _a = this.props, params = _a.params, location = _a.location;
        return [
            [
                'eventAttachments',
                "/issues/" + params.groupId + "/attachments/",
                {
                    query: tslib_1.__assign(tslib_1.__assign({}, pick_1.default(location.query, ['cursor', 'environment', 'types'])), { limit: 50 }),
                },
            ],
        ];
    };
    GroupEventAttachments.prototype.renderNoQueryResults = function () {
        return (<emptyStateWarning_1.default>
        <p>{locale_1.t('Sorry, no event attachments match your search query.')}</p>
      </emptyStateWarning_1.default>);
    };
    GroupEventAttachments.prototype.renderEmpty = function () {
        return (<emptyStateWarning_1.default>
        <p>{locale_1.t("There don't seem to be any event attachments yet.")}</p>
      </emptyStateWarning_1.default>);
    };
    GroupEventAttachments.prototype.renderLoading = function () {
        return this.renderBody();
    };
    GroupEventAttachments.prototype.renderInnerBody = function () {
        var _a = this.props, projectSlug = _a.projectSlug, params = _a.params, location = _a.location;
        var _b = this.state, loading = _b.loading, eventAttachments = _b.eventAttachments, deletedAttachments = _b.deletedAttachments;
        if (loading) {
            return <loadingIndicator_1.default />;
        }
        if (eventAttachments.length > 0) {
            return (<groupEventAttachmentsTable_1.default attachments={eventAttachments} orgId={params.orgId} projectId={projectSlug} groupId={params.groupId} onDelete={this.handleDelete} deletedAttachments={deletedAttachments}/>);
        }
        if (location.query.types) {
            return this.renderNoQueryResults();
        }
        return this.renderEmpty();
    };
    GroupEventAttachments.prototype.renderBody = function () {
        return (<react_1.Fragment>
        <groupEventAttachmentsFilter_1.default />
        <panels_1.Panel className="event-list">
          <panels_1.PanelBody>{this.renderInnerBody()}</panels_1.PanelBody>
        </panels_1.Panel>
        <pagination_1.default pageLinks={this.state.eventAttachmentsPageLinks}/>
      </react_1.Fragment>);
    };
    return GroupEventAttachments;
}(asyncComponent_1.default));
exports.default = ReactRouter.withRouter(GroupEventAttachments);
//# sourceMappingURL=groupEventAttachments.jsx.map