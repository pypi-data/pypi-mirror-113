Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var enzyme_1 = require("sentry-test/enzyme");
var bulkController_1 = tslib_1.__importDefault(require("app/components/bulkController"));
function renderedComponent(renderProp, pageIds, defaultSelectedIds) {
    return enzyme_1.shallow(<bulkController_1.default allRowsCount={32} pageIds={pageIds} defaultSelectedIds={defaultSelectedIds} columnsCount={4}>
      {function (_a) {
            var isAllSelected = _a.isAllSelected, isPageSelected = _a.isPageSelected, selectedIds = _a.selectedIds, onRowToggle = _a.onRowToggle, onAllRowsToggle = _a.onAllRowsToggle, onPageRowsToggle = _a.onPageRowsToggle;
            renderProp(isAllSelected, isPageSelected, selectedIds);
            return (<react_1.Fragment>
            {isPageSelected && 'whole page selected'}
            {isAllSelected && 'everything selected'}
            <button data-test-id="selectAll" onClick={function () { return onAllRowsToggle(true); }}/>
            <button data-test-id="selectPage" onClick={function () { return onPageRowsToggle(true); }}/>
            <button data-test-id="unselectAll" onClick={function () { return onAllRowsToggle(false); }}/>
            <button data-test-id="deselectPage" onClick={function () { return onPageRowsToggle(false); }}/>
            <button data-test-id="toggleRow" onClick={function () { return onRowToggle('2'); }}/>
          </react_1.Fragment>);
        }}
    </bulkController_1.default>);
}
describe('BulkController', function () {
    var pageIds = ['1', '2', '3'];
    var renderProp = jest.fn();
    var wrapper, toggleRow, selectPage, deselectPage, selectAll, unselectAll;
    describe('renders', function () {
        beforeEach(function () {
            wrapper = renderedComponent(renderProp, pageIds);
            toggleRow = wrapper.find('[data-test-id="toggleRow"]');
            selectPage = wrapper.find('[data-test-id="selectPage"]');
            deselectPage = wrapper.find('[data-test-id="deselectPage"]');
            selectAll = wrapper.find('[data-test-id="selectAll"]');
            unselectAll = wrapper.find('[data-test-id="unselectAll"]');
        });
        it('sets the defaults', function () {
            expect(renderProp).toHaveBeenLastCalledWith(false, false, []);
        });
        it('toggles single item', function () {
            toggleRow.simulate('click');
            expect(renderProp).toHaveBeenLastCalledWith(false, false, ['2']);
            toggleRow.simulate('click');
            expect(renderProp).toHaveBeenLastCalledWith(false, false, []);
        });
        it('toggles the page', function () {
            toggleRow.simulate('click');
            expect(renderProp).toHaveBeenLastCalledWith(false, false, ['2']);
            selectPage.simulate('click');
            expect(renderProp).toHaveBeenLastCalledWith(false, true, ['2', '1', '3']);
            deselectPage.simulate('click');
            expect(renderProp).toHaveBeenLastCalledWith(false, false, []);
        });
        it('toggles everything', function () {
            toggleRow.simulate('click');
            expect(renderProp).toHaveBeenLastCalledWith(false, false, ['2']);
            selectAll.simulate('click');
            expect(renderProp).toHaveBeenLastCalledWith(true, true, ['1', '2', '3']);
            unselectAll.simulate('click');
            expect(renderProp).toHaveBeenLastCalledWith(false, false, []);
        });
        it('deselects one after having everything selected', function () {
            selectAll.simulate('click');
            expect(renderProp).toHaveBeenLastCalledWith(true, true, ['1', '2', '3']);
            toggleRow.simulate('click');
            expect(renderProp).toHaveBeenLastCalledWith(false, false, ['1', '3']);
        });
    });
    describe('with default selectIds', function () {
        it('sets the defaults', function () {
            wrapper = renderedComponent(renderProp, pageIds, ['2']);
            expect(renderProp).toHaveBeenLastCalledWith(false, false, ['2']);
        });
        it('page is selected by default', function () {
            wrapper = renderedComponent(renderProp, pageIds, pageIds);
            expect(renderProp).toHaveBeenLastCalledWith(false, true, pageIds);
        });
        it('toggle the last unchecked option, should change button selectAll to true', function () {
            var defaultSelectedIds = ['1', '3'];
            wrapper = renderedComponent(renderProp, pageIds, defaultSelectedIds);
            expect(renderProp).toHaveBeenLastCalledWith(false, false, defaultSelectedIds);
            toggleRow.simulate('click');
            expect(renderProp).toHaveBeenLastCalledWith(false, true, tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(defaultSelectedIds)), [
                '2',
            ]));
        });
    });
});
//# sourceMappingURL=index.spec.jsx.map