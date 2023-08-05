Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var react_virtualized_1 = require("react-virtualized");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var modal_1 = require("app/actionCreators/modal");
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var eventDataSection_1 = tslib_1.__importDefault(require("app/components/events/eventDataSection"));
var utils_1 = require("app/components/events/interfaces/utils");
var panels_1 = require("app/components/panels");
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var locale_1 = require("app/locale");
var debugMetaStore_1 = tslib_1.__importStar(require("app/stores/debugMetaStore"));
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var debugImage_1 = require("app/types/debugImage");
var utils_2 = require("app/utils");
var searchBarAction_1 = tslib_1.__importDefault(require("../searchBarAction"));
var searchBarActionFilter_1 = tslib_1.__importDefault(require("../searchBarAction/searchBarActionFilter"));
var status_1 = tslib_1.__importDefault(require("./debugImage/status"));
var debugImage_2 = tslib_1.__importDefault(require("./debugImage"));
var layout_1 = tslib_1.__importDefault(require("./layout"));
var utils_3 = require("./utils");
var IMAGE_INFO_UNAVAILABLE = '-1';
var cache = new react_virtualized_1.CellMeasurerCache({
    fixedWidth: true,
    defaultHeight: 81,
});
var DebugMeta = /** @class */ (function (_super) {
    tslib_1.__extends(DebugMeta, _super);
    function DebugMeta() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            searchTerm: '',
            scrollbarWidth: 0,
            filterOptions: {},
            filteredImages: [],
            filteredImagesByFilter: [],
            filteredImagesBySearch: [],
        };
        _this.panelTableRef = React.createRef();
        _this.listRef = null;
        _this.onDebugMetaStoreChange = function (store) {
            var searchTerm = _this.state.searchTerm;
            if (store.filter !== searchTerm) {
                _this.setState({ searchTerm: store.filter }, _this.filterImagesBySearchTerm);
            }
        };
        _this.updateGrid = function () {
            if (_this.listRef) {
                cache.clearAll();
                _this.listRef.forceUpdateGrid();
                _this.getScrollbarWidth();
            }
        };
        _this.openImageDetailsModal = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var filteredImages, _a, location, organization, projectId, groupId, event, query, imageCodeId, imageDebugId, image, mod, Modal, modalCss;
            var _this = this;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        filteredImages = this.state.filteredImages;
                        if (!filteredImages.length) {
                            return [2 /*return*/];
                        }
                        _a = this.props, location = _a.location, organization = _a.organization, projectId = _a.projectId, groupId = _a.groupId, event = _a.event;
                        query = location.query;
                        imageCodeId = query.imageCodeId, imageDebugId = query.imageDebugId;
                        if (!imageCodeId && !imageDebugId) {
                            return [2 /*return*/];
                        }
                        image = imageCodeId !== IMAGE_INFO_UNAVAILABLE || imageDebugId !== IMAGE_INFO_UNAVAILABLE
                            ? filteredImages.find(function (_a) {
                                var code_id = _a.code_id, debug_id = _a.debug_id;
                                return code_id === imageCodeId || debug_id === imageDebugId;
                            })
                            : undefined;
                        return [4 /*yield*/, Promise.resolve().then(function () { return tslib_1.__importStar(require('app/components/events/interfaces/debugMeta-v2/debugImageDetails')); })];
                    case 1:
                        mod = _b.sent();
                        Modal = mod.default, modalCss = mod.modalCss;
                        modal_1.openModal(function (deps) { return (<Modal {...deps} image={image} organization={organization} projectId={projectId} event={event} onReprocessEvent={utils_2.defined(groupId) ? _this.handleReprocessEvent(groupId) : undefined}/>); }, {
                            modalCss: modalCss,
                            onClose: this.handleCloseImageDetailsModal,
                        });
                        return [2 /*return*/];
                }
            });
        }); };
        _this.handleChangeFilter = function (filterOptions) {
            var filteredImagesBySearch = _this.state.filteredImagesBySearch;
            var filteredImagesByFilter = _this.getFilteredImagesByFilter(filteredImagesBySearch, filterOptions);
            _this.setState({ filterOptions: filterOptions, filteredImagesByFilter: filteredImagesByFilter }, _this.updateGrid);
        };
        _this.handleChangeSearchTerm = function (searchTerm) {
            if (searchTerm === void 0) { searchTerm = ''; }
            debugMetaStore_1.DebugMetaActions.updateFilter(searchTerm);
        };
        _this.handleResetFilter = function () {
            var filterOptions = _this.state.filterOptions;
            _this.setState({
                filterOptions: Object.keys(filterOptions).reduce(function (accumulator, currentValue) {
                    accumulator[currentValue] = filterOptions[currentValue].map(function (filterOption) { return (tslib_1.__assign(tslib_1.__assign({}, filterOption), { isChecked: false })); });
                    return accumulator;
                }, {}),
            }, _this.filterImagesBySearchTerm);
        };
        _this.handleResetSearchBar = function () {
            _this.setState(function (prevState) { return ({
                searchTerm: '',
                filteredImagesByFilter: prevState.filteredImages,
                filteredImagesBySearch: prevState.filteredImages,
            }); });
        };
        _this.handleOpenImageDetailsModal = function (code_id, debug_id) {
            var _a = _this.props, location = _a.location, router = _a.router;
            router.push(tslib_1.__assign(tslib_1.__assign({}, location), { query: tslib_1.__assign(tslib_1.__assign({}, location.query), { imageCodeId: code_id !== null && code_id !== void 0 ? code_id : IMAGE_INFO_UNAVAILABLE, imageDebugId: debug_id !== null && debug_id !== void 0 ? debug_id : IMAGE_INFO_UNAVAILABLE }) }));
        };
        _this.handleCloseImageDetailsModal = function () {
            var _a = _this.props, location = _a.location, router = _a.router;
            router.push(tslib_1.__assign(tslib_1.__assign({}, location), { query: tslib_1.__assign(tslib_1.__assign({}, location.query), { imageCodeId: undefined, imageDebugId: undefined }) }));
        };
        _this.handleReprocessEvent = function (groupId) { return function () {
            var organization = _this.props.organization;
            modal_1.openReprocessEventModal({
                organization: organization,
                groupId: groupId,
                onClose: _this.openImageDetailsModal,
            });
        }; };
        _this.renderRow = function (_a) {
            var index = _a.index, key = _a.key, parent = _a.parent, style = _a.style;
            var images = _this.state.filteredImagesByFilter;
            return (<react_virtualized_1.CellMeasurer cache={cache} columnIndex={0} key={key} parent={parent} rowIndex={index}>
        <debugImage_2.default style={style} image={images[index]} onOpenImageDetailsModal={_this.handleOpenImageDetailsModal}/>
      </react_virtualized_1.CellMeasurer>);
        };
        return _this;
    }
    DebugMeta.prototype.componentDidMount = function () {
        this.unsubscribeFromDebugMetaStore = debugMetaStore_1.default.listen(this.onDebugMetaStoreChange, undefined);
        cache.clearAll();
        this.getRelevantImages();
        this.openImageDetailsModal();
    };
    DebugMeta.prototype.componentDidUpdate = function (_prevProps, prevState) {
        if (prevState.filteredImages.length === 0 && this.state.filteredImages.length > 0) {
            this.getPanelBodyHeight();
        }
        this.openImageDetailsModal();
    };
    DebugMeta.prototype.componentWillUnmount = function () {
        if (this.unsubscribeFromDebugMetaStore) {
            this.unsubscribeFromDebugMetaStore();
        }
    };
    DebugMeta.prototype.getScrollbarWidth = function () {
        var _a, _b, _c, _d, _e, _f, _g;
        var panelTableWidth = (_c = (_b = (_a = this.panelTableRef) === null || _a === void 0 ? void 0 : _a.current) === null || _b === void 0 ? void 0 : _b.clientWidth) !== null && _c !== void 0 ? _c : 0;
        var gridInnerWidth = (_g = (_f = (_e = (_d = this.panelTableRef) === null || _d === void 0 ? void 0 : _d.current) === null || _e === void 0 ? void 0 : _e.querySelector('.ReactVirtualized__Grid__innerScrollContainer')) === null || _f === void 0 ? void 0 : _f.clientWidth) !== null && _g !== void 0 ? _g : 0;
        var scrollbarWidth = panelTableWidth - gridInnerWidth;
        if (scrollbarWidth !== this.state.scrollbarWidth) {
            this.setState({ scrollbarWidth: scrollbarWidth });
        }
    };
    DebugMeta.prototype.isValidImage = function (image) {
        // in particular proguard images do not have a code file, skip them
        if (image === null || image.code_file === null || image.type === 'proguard') {
            return false;
        }
        if (utils_3.getFileName(image.code_file) === 'dyld_sim') {
            // this is only for simulator builds
            return false;
        }
        return true;
    };
    DebugMeta.prototype.filterImage = function (image, searchTerm) {
        var _a, _b;
        // When searching for an address, check for the address range of the image
        // instead of an exact match.  Note that images cannot be found by index
        // if they are at 0x0.  For those relative addressing has to be used.
        if (searchTerm.indexOf('0x') === 0) {
            var needle = utils_1.parseAddress(searchTerm);
            if (needle > 0 && image.image_addr !== '0x0') {
                var _c = tslib_1.__read(utils_1.getImageRange(image), 2), startAddress = _c[0], endAddress = _c[1]; // TODO(PRISCILA): remove any
                return needle >= startAddress && needle < endAddress;
            }
        }
        // the searchTerm ending at "!" is the end of the ID search.
        var relMatch = searchTerm.match(/^\s*(.*?)!/); // debug_id!address
        var idSearchTerm = utils_3.normalizeId((relMatch === null || relMatch === void 0 ? void 0 : relMatch[1]) || searchTerm);
        return (
        // Prefix match for identifiers
        utils_3.normalizeId(image.code_id).indexOf(idSearchTerm) === 0 ||
            utils_3.normalizeId(image.debug_id).indexOf(idSearchTerm) === 0 ||
            // Any match for file paths
            (((_a = image.code_file) === null || _a === void 0 ? void 0 : _a.toLowerCase()) || '').indexOf(searchTerm) >= 0 ||
            (((_b = image.debug_file) === null || _b === void 0 ? void 0 : _b.toLowerCase()) || '').indexOf(searchTerm) >= 0);
    };
    DebugMeta.prototype.filterImagesBySearchTerm = function () {
        var _this = this;
        var _a = this.state, filteredImages = _a.filteredImages, filterOptions = _a.filterOptions, searchTerm = _a.searchTerm;
        var filteredImagesBySearch = filteredImages.filter(function (image) {
            return _this.filterImage(image, searchTerm.toLowerCase());
        });
        var filteredImagesByFilter = this.getFilteredImagesByFilter(filteredImagesBySearch, filterOptions);
        this.setState({
            filteredImagesBySearch: filteredImagesBySearch,
            filteredImagesByFilter: filteredImagesByFilter,
        }, this.updateGrid);
    };
    DebugMeta.prototype.getPanelBodyHeight = function () {
        var _a, _b;
        var panelTableHeight = (_b = (_a = this.panelTableRef) === null || _a === void 0 ? void 0 : _a.current) === null || _b === void 0 ? void 0 : _b.offsetHeight;
        if (!panelTableHeight) {
            return;
        }
        this.setState({ panelTableHeight: panelTableHeight });
    };
    DebugMeta.prototype.getRelevantImages = function () {
        var data = this.props.data;
        var images = data.images;
        // There are a bunch of images in debug_meta that are not relevant to this
        // component. Filter those out to reduce the noise. Most importantly, this
        // includes proguard images, which are rendered separately.
        var relevantImages = images.filter(this.isValidImage);
        if (!relevantImages.length) {
            return;
        }
        var formattedRelevantImages = relevantImages.map(function (releventImage) {
            var _a = releventImage, debug_status = _a.debug_status, unwind_status = _a.unwind_status;
            return tslib_1.__assign(tslib_1.__assign({}, releventImage), { status: utils_3.combineStatus(debug_status, unwind_status) });
        });
        // Sort images by their start address. We assume that images have
        // non-overlapping ranges. Each address is given as hex string (e.g.
        // "0xbeef").
        formattedRelevantImages.sort(function (a, b) { return utils_1.parseAddress(a.image_addr) - utils_1.parseAddress(b.image_addr); });
        var unusedImages = [];
        var usedImages = formattedRelevantImages.filter(function (image) {
            if (image.debug_status === debugImage_1.ImageStatus.UNUSED) {
                unusedImages.push(image);
                return false;
            }
            return true;
        });
        var filteredImages = tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(usedImages)), tslib_1.__read(unusedImages));
        var filterOptions = this.getFilterOptions(filteredImages);
        this.setState({
            filteredImages: filteredImages,
            filterOptions: filterOptions,
            filteredImagesByFilter: this.getFilteredImagesByFilter(filteredImages, filterOptions),
            filteredImagesBySearch: filteredImages,
        });
    };
    DebugMeta.prototype.getFilterOptions = function (images) {
        var _a;
        return _a = {},
            _a[locale_1.t('Status')] = tslib_1.__spreadArray([], tslib_1.__read(new Set(images.map(function (image) { return image.status; })))).map(function (status) { return ({
                id: status,
                symbol: <status_1.default status={status}/>,
                isChecked: status !== debugImage_1.ImageStatus.UNUSED,
            }); }),
            _a;
    };
    DebugMeta.prototype.getFilteredImagesByFilter = function (filteredImages, filterOptions) {
        var checkedOptions = new Set(Object.values(filterOptions)[0]
            .filter(function (filterOption) { return filterOption.isChecked; })
            .map(function (option) { return option.id; }));
        if (!tslib_1.__spreadArray([], tslib_1.__read(checkedOptions)).length) {
            return filteredImages;
        }
        return filteredImages.filter(function (image) { return checkedOptions.has(image.status); });
    };
    DebugMeta.prototype.renderList = function () {
        var _this = this;
        var _a = this.state, images = _a.filteredImagesByFilter, panelTableHeight = _a.panelTableHeight;
        if (!panelTableHeight) {
            return images.map(function (image, index) { return (<debugImage_2.default key={index} image={image} onOpenImageDetailsModal={_this.handleOpenImageDetailsModal}/>); });
        }
        return (<react_virtualized_1.AutoSizer disableHeight onResize={this.updateGrid}>
        {function (_a) {
                var width = _a.width;
                return (<StyledList ref={function (el) {
                        _this.listRef = el;
                    }} deferredMeasurementCache={cache} height={utils_3.IMAGE_AND_CANDIDATE_LIST_MAX_HEIGHT} overscanRowCount={5} rowCount={images.length} rowHeight={cache.rowHeight} rowRenderer={_this.renderRow} width={width} isScrolling={false}/>);
            }}
      </react_virtualized_1.AutoSizer>);
    };
    DebugMeta.prototype.getEmptyMessage = function () {
        var _a = this.state, searchTerm = _a.searchTerm, images = _a.filteredImagesByFilter, filterOptions = _a.filterOptions;
        if (!!images.length) {
            return {};
        }
        if (searchTerm && !images.length) {
            var hasActiveFilter = Object.values(filterOptions)
                .flatMap(function (filterOption) { return filterOption; })
                .find(function (filterOption) { return filterOption.isChecked; });
            return {
                emptyMessage: locale_1.t('Sorry, no images match your search query'),
                emptyAction: hasActiveFilter ? (<button_1.default onClick={this.handleResetFilter} priority="primary">
            {locale_1.t('Reset filter')}
          </button_1.default>) : (<button_1.default onClick={this.handleResetSearchBar} priority="primary">
            {locale_1.t('Clear search bar')}
          </button_1.default>),
            };
        }
        return {
            emptyMessage: locale_1.t('There are no images to be displayed'),
        };
    };
    DebugMeta.prototype.render = function () {
        var _this = this;
        var _a;
        var _b = this.state, searchTerm = _b.searchTerm, filterOptions = _b.filterOptions, scrollbarWidth = _b.scrollbarWidth, filteredImages = _b.filteredImagesByFilter;
        var data = this.props.data;
        var images = data.images;
        if (utils_3.shouldSkipSection(filteredImages, images)) {
            return null;
        }
        var displayFilter = ((_a = Object.values(filterOptions !== null && filterOptions !== void 0 ? filterOptions : {})[0]) !== null && _a !== void 0 ? _a : []).length > 1;
        return (<StyledEventDataSection type="images-loaded" title={<TitleWrapper>
            <guideAnchor_1.default target="images-loaded" position="bottom">
              <Title>{locale_1.t('Images Loaded')}</Title>
            </guideAnchor_1.default>
            <questionTooltip_1.default size="xs" position="top" title={locale_1.t('A list of dynamic librarys or shared objects loaded into process memory at the time of the crash. Images contribute application code that is referenced in stack traces.')}/>
          </TitleWrapper>} actions={<StyledSearchBarAction placeholder={locale_1.t('Search images loaded')} onChange={function (value) { return _this.handleChangeSearchTerm(value); }} query={searchTerm} filter={displayFilter ? (<searchBarActionFilter_1.default onChange={this.handleChangeFilter} options={filterOptions}/>) : undefined}/>} wrapTitle={false} isCentered>
        <StyledPanelTable isEmpty={!filteredImages.length} scrollbarWidth={scrollbarWidth} headers={[locale_1.t('Status'), locale_1.t('Image'), locale_1.t('Processing'), locale_1.t('Details'), '']} {...this.getEmptyMessage()}>
          <div ref={this.panelTableRef}>{this.renderList()}</div>
        </StyledPanelTable>
      </StyledEventDataSection>);
    };
    DebugMeta.defaultProps = {
        data: { images: [] },
    };
    return DebugMeta;
}(React.PureComponent));
exports.default = react_router_1.withRouter(DebugMeta);
var StyledEventDataSection = styled_1.default(eventDataSection_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding-bottom: ", ";\n\n  /* to increase specificity */\n  @media (min-width: ", ") {\n    padding-bottom: ", ";\n  }\n"], ["\n  padding-bottom: ", ";\n\n  /* to increase specificity */\n  @media (min-width: ", ") {\n    padding-bottom: ", ";\n  }\n"])), space_1.default(4), function (p) { return p.theme.breakpoints[0]; }, space_1.default(2));
var StyledPanelTable = styled_1.default(panels_1.PanelTable)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  overflow: hidden;\n  > * {\n    :nth-child(-n + 5) {\n      ", ";\n      border-bottom: 1px solid ", ";\n      :nth-child(5n) {\n        height: 100%;\n        ", "\n      }\n    }\n\n    :nth-child(n + 6) {\n      grid-column: 1/-1;\n      ", "\n    }\n  }\n\n  ", "\n"], ["\n  overflow: hidden;\n  > * {\n    :nth-child(-n + 5) {\n      ", ";\n      border-bottom: 1px solid ", ";\n      :nth-child(5n) {\n        height: 100%;\n        ", "\n      }\n    }\n\n    :nth-child(n + 6) {\n      grid-column: 1/-1;\n      ", "\n    }\n  }\n\n  ", "\n"])), overflowEllipsis_1.default, function (p) { return p.theme.border; }, function (p) { return !p.scrollbarWidth && "display: none"; }, function (p) {
    return !p.isEmpty &&
        "\n          display: grid;\n          padding: 0;\n        ";
}, function (p) { return layout_1.default(p.theme, p.scrollbarWidth); });
var TitleWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  padding: ", " 0;\n"], ["\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  padding: ", " 0;\n"])), space_1.default(0.5), space_1.default(0.75));
var Title = styled_1.default('h3')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin-bottom: 0;\n  padding: 0 !important;\n  height: 14px;\n"], ["\n  margin-bottom: 0;\n  padding: 0 !important;\n  height: 14px;\n"])));
// XXX(ts): Emotion11 has some trouble with List's defaultProps
var StyledList = styled_1.default(react_virtualized_1.List)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  height: auto !important;\n  max-height: ", "px;\n  overflow-y: auto !important;\n  outline: none;\n"], ["\n  height: auto !important;\n  max-height: ", "px;\n  overflow-y: auto !important;\n  outline: none;\n"])), function (p) { return p.height; });
var StyledSearchBarAction = styled_1.default(searchBarAction_1.default)(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  z-index: 1;\n"], ["\n  z-index: 1;\n"])));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=index.jsx.map